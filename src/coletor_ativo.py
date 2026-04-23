"""
OfertaHub — Coletor Híbrido (SCAFFOLD INATIVO)

⚠ Este módulo NÃO é importado pelo pipeline atual. Serve como esqueleto
  arquitetural para quando uma fonte de dados real estiver disponível
  (PA-API aprovada OU proxy residencial contratado).

Motivo do congelamento (validado em 2026-04-22):
  - Feeds RSS de agregadores BR (Pelando, Promobit, MeuHunter, Bondfaro)
    retornam 404/500/DNS-fail. Todos descontinuaram RSS público após
    migração para SPAs + monetização via redirect próprio.
  - Scraping direto de /dp/{ASIN} a partir de IPs residenciais retorna
    página de CAPTCHA já na primeira requisição (Amazon classifica o
    host como automated).

Re-validado em 2026-04-23:
  - Raio-X estrutural (tests/raio_x_feed.py) confirma HTTP 404 em
    pelando.com.br/rss e promobit.com.br/rss/hot/. Content-Type devolvido
    é text/html (páginas de erro), não RSS.
  - Scaffold permanece congelado à espera da aprovação PA-API (Opção A).

Estratégia original (mantida para referência):
  1. RSS de agregadores → descobre ASINs candidatos.
  2. Scraping de /dp/{ASIN} → extrai título, preço, nota, avaliações, imagem.
  3. Fallback para mock_api se ambos falharem.

Como reativar:
  - Opção A (PA-API): preencher AMAZON_API em config.py, substituir
    `_FEEDS_DESCOBERTA` pela chamada à API Amazon e trocar import no
    pipeline.py para `from coletor_ativo import buscar_produtos`.
  - Opção B (Proxy residencial): injetar `proxies={...}` em `_fetch()`
    e rodar isoladamente para validar taxa de sucesso antes de religar.

Regra de ouro preservada: campos críticos ausentes → produto descartado.
Nunca inventamos preço, nota ou avaliações — dados fictícios fraudariam
o Gerente IA.
"""

from __future__ import annotations

import concurrent.futures
import logging
import random
import re
import time
from dataclasses import dataclass
from urllib.parse import urlparse
from urllib.robotparser import RobotFileParser

import feedparser
import requests
from bs4 import BeautifulSoup

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [COLETOR] %(message)s",
)
logger = logging.getLogger("coletor")


# ── Configuração ──────────────────────────────────────────────────────────

_USER_AGENTS = [
    "Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:120.0) Gecko/20100101 Firefox/120.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 "
    "(KHTML, like Gecko) Version/17.1 Safari/605.1.15",
]

_HEADERS_BASE = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "pt-BR,pt;q=0.9,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "DNT": "1",
    "Upgrade-Insecure-Requests": "1",
}

# Feeds RSS públicos de agregadores — não são fontes oficiais Amazon.
_FEEDS_DESCOBERTA = [
    "https://www.pelando.com.br/rss",
    "https://www.promobit.com.br/rss/hot/",
]

# Regex para pescar ASIN em QUALQUER URL Amazon conhecido.
# Formatos cobertos: /dp/B0XXX, /gp/product/B0XXX, /product/B0XXX, /o/ASIN/B0XXX
_ASIN_RE = re.compile(r"/(?:dp|gp/product|product|o/ASIN)/([A-Z0-9]{10})")

# Circuit breaker: depois de N 503 consecutivos, desistimos do scraping no ciclo.
_MAX_503_CONSECUTIVOS = 3
_TIMEOUT_HTTP = 10
_SLEEP_ENTRE_REQS = (1.5, 3.0)   # jitter uniforme (s) entre requests à Amazon


# ── robots.txt cache ──────────────────────────────────────────────────────

_robots_cache: dict[str, RobotFileParser] = {}


def _robots_permite(url: str) -> bool:
    """Respeita /robots.txt do host antes de qualquer GET."""
    host = urlparse(url).netloc
    if host not in _robots_cache:
        rp = RobotFileParser()
        rp.set_url(f"https://{host}/robots.txt")
        try:
            rp.read()
        except Exception as exc:
            logger.warning("robots.txt indisponível em %s: %s — bloqueando por precaução.", host, exc)
            return False
        _robots_cache[host] = rp
    return _robots_cache[host].can_fetch(_USER_AGENTS[0], url)


# ── Fetch com backoff + rotação de UA ─────────────────────────────────────

@dataclass
class _FetchState:
    """Estado compartilhado entre chamadas no mesmo ciclo (circuit breaker)."""
    falhas_503_consecutivas: int = 0

    def bloqueado(self) -> bool:
        return self.falhas_503_consecutivas >= _MAX_503_CONSECUTIVOS


def _fetch(url: str, estado: _FetchState, tentativas: int = 2) -> str | None:
    """GET com rotação de User-Agent, backoff exponencial e circuit breaker."""
    if estado.bloqueado():
        return None
    if not _robots_permite(url):
        logger.warning("robots.txt proíbe: %s", url)
        return None

    for tentativa in range(tentativas):
        headers = {**_HEADERS_BASE, "User-Agent": random.choice(_USER_AGENTS)}
        try:
            resp = requests.get(url, headers=headers, timeout=_TIMEOUT_HTTP, allow_redirects=True)
        except requests.RequestException as exc:
            logger.warning("Erro de rede em %s (tentativa %d): %s", url, tentativa + 1, exc)
            time.sleep(2 ** tentativa)
            continue

        if resp.status_code == 200:
            estado.falhas_503_consecutivas = 0
            return resp.text
        if resp.status_code == 503:
            estado.falhas_503_consecutivas += 1
            logger.warning("503 em %s — possível captcha/bloqueio (%d/%d).",
                           url, estado.falhas_503_consecutivas, _MAX_503_CONSECUTIVOS)
            if estado.bloqueado():
                return None
            time.sleep((2 ** tentativa) + random.random())
            continue
        logger.info("HTTP %d em %s — pulando.", resp.status_code, url)
        return None

    return None


def _resolver_redirect(url: str) -> str:
    """HEAD seguindo redirects para desofuscar shorteners (pelan.do, bit.ly…)."""
    try:
        resp = requests.head(url, headers={**_HEADERS_BASE, "User-Agent": _USER_AGENTS[0]},
                             timeout=5, allow_redirects=True)
        return resp.url
    except requests.RequestException:
        return url


# ── Etapa 1: descoberta de ASINs via RSS ──────────────────────────────────

def _extrair_asins_do_texto(texto: str) -> list[str]:
    return _ASIN_RE.findall(texto or "")


def descobrir_asins_via_rss(limite: int = 20) -> list[str]:
    """
    Varre feeds RSS públicos e devolve ASINs únicos mencionados.

    Estratégia em duas passagens:
      1. Passagem barata (sem I/O): regex sobre título + summary + link
         direto. O que for capturável aqui nunca precisa de rede.
      2. Passagem paralela (I/O-bound): links que não revelaram ASIN são
         resolvidos via HEAD num ThreadPoolExecutor (max_workers=5), para
         desofuscar shorteners (pelan.do, bit.ly, etc.) sem empilhar
         latências sequenciais.
    """
    asins: list[str] = []
    vistos: set[str] = set()
    links_pendentes: list[str] = []

    # ── Passagem 1: extração directa do conteúdo já presente no feed ──
    for feed_url in _FEEDS_DESCOBERTA:
        logger.info("Lendo feed: %s", feed_url)
        try:
            resp = requests.get(
                feed_url,
                headers={**_HEADERS_BASE, "User-Agent": _USER_AGENTS[0]},
                timeout=_TIMEOUT_HTTP,
            )
            if resp.status_code != 200:
                logger.warning(
                    "Feed %s devolveu HTTP %d — ignorando.",
                    feed_url, resp.status_code,
                )
                continue
            feed = feedparser.parse(resp.content)
        except Exception as exc:
            logger.error("Falha ao ler %s: %s", feed_url, exc)
            continue

        # Cap defensivo: nunca processamos mais do que o dobro do limite
        # de entradas por feed — evita varrer feeds gigantes inteiros.
        for entrada in feed.entries[: limite * 2]:
            if len(asins) >= limite:
                return asins

            blob = " ".join(filter(None, [
                entrada.get("title"),
                entrada.get("summary"),
                entrada.get("link"),
            ]))

            achados = _extrair_asins_do_texto(blob)
            if achados:
                for asin in achados:
                    if asin not in vistos:
                        vistos.add(asin)
                        asins.append(asin)
                        if len(asins) >= limite:
                            return asins
            elif entrada.get("link"):
                # ASIN está escondido atrás de shortener — adia para
                # a passagem paralela em vez de bloquear já.
                links_pendentes.append(entrada["link"])

    if not links_pendentes:
        logger.info("Descoberta RSS: %d ASINs únicos (nenhum redirect necessário).", len(asins))
        return asins

    # ── Passagem 2: resolução paralela dos links ofuscados ──
    logger.info(
        "A resolver %d links ofuscados em paralelo (max_workers=5)...",
        len(links_pendentes),
    )
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:
        futuros = {pool.submit(_resolver_redirect, link): link for link in links_pendentes}
        for futuro in concurrent.futures.as_completed(futuros):
            if len(asins) >= limite:
                break
            try:
                destino = futuro.result()
            except Exception as exc:
                # Uma falha de thread não pode derrubar as outras.
                logger.debug("Redirect falhou em %s: %s", futuros[futuro], exc)
                continue

            for asin in _extrair_asins_do_texto(destino):
                if asin not in vistos:
                    vistos.add(asin)
                    asins.append(asin)
                    if len(asins) >= limite:
                        break

    logger.info("Descoberta RSS: %d ASINs únicos.", len(asins))
    return asins


# ── Etapa 2: enriquecimento via scraping da página do produto ─────────────

def _parse_preco(texto: str | None) -> float | None:
    """Converte 'R$ 1.299,00' → 1299.00. Devolve None se malformado."""
    if not texto:
        return None
    m = re.search(r"(\d{1,3}(?:\.\d{3})*,\d{2}|\d+,\d{2}|\d+\.\d{2}|\d+)", texto)
    if not m:
        return None
    bruto = m.group(1).replace(".", "").replace(",", ".")
    try:
        return float(bruto)
    except ValueError:
        return None


def _parse_inteiro(texto: str | None) -> int | None:
    """Converte '18.420 avaliações' → 18420."""
    if not texto:
        return None
    m = re.search(r"([\d\.]+)", texto)
    if not m:
        return None
    try:
        return int(m.group(1).replace(".", ""))
    except ValueError:
        return None


def _parse_nota(texto: str | None) -> float | None:
    """Converte '4,7 de 5 estrelas' → 4.7."""
    if not texto:
        return None
    m = re.search(r"(\d+[,.]\d)", texto)
    return float(m.group(1).replace(",", ".")) if m else None


def enriquecer_asin(asin: str, estado: _FetchState) -> dict | None:
    """
    Baixa /dp/{ASIN} e extrai título, preço atual, preço original, nota,
    avaliações e imagem. Retorna None se qualquer campo crítico faltar —
    o chamador não precisa validar, basta descartar None.
    """
    url = f"https://www.amazon.com.br/dp/{asin}"
    html = _fetch(url, estado)
    if not html:
        return None

    soup = BeautifulSoup(html, "lxml")

    titulo_el = soup.select_one("#productTitle")
    preco_atual_el = soup.select_one(".a-price .a-offscreen")
    # Preço "de": preço riscado de referência
    preco_orig_el = soup.select_one(
        "span.a-price.a-text-price[data-a-strike='true'] .a-offscreen"
    ) or soup.select_one(".basisPrice .a-offscreen")
    nota_el = soup.select_one("span[data-hook='rating-out-of-text']") \
        or soup.select_one("#acrPopover span.a-icon-alt")
    avals_el = soup.select_one("#acrCustomerReviewText")
    img_el = soup.select_one("#landingImage") or soup.select_one("#imgTagWrapperId img")
    breadcrumb_el = soup.select_one("#wayfinding-breadcrumbs_feature_div a")

    titulo = titulo_el.get_text(strip=True) if titulo_el else None
    preco_atual = _parse_preco(preco_atual_el.get_text() if preco_atual_el else None)
    preco_original = _parse_preco(preco_orig_el.get_text() if preco_orig_el else None)
    nota = _parse_nota(nota_el.get_text() if nota_el else None)
    total_avaliacoes = _parse_inteiro(avals_el.get_text() if avals_el else None)
    imagem = img_el.get("src") if img_el else None
    categoria = breadcrumb_el.get_text(strip=True) if breadcrumb_el else "Geral"

    # Sem preço original, não há desconto comparável → não é oferta.
    if preco_original is None or preco_original <= preco_atual:
        logger.debug("ASIN %s descartado: sem preço de referência.", asin)
        return None

    criticos = {"titulo": titulo, "preco_atual": preco_atual, "nota": nota,
                "total_avaliacoes": total_avaliacoes}
    faltando = [k for k, v in criticos.items() if v is None]
    if faltando:
        logger.debug("ASIN %s descartado: faltam %s.", asin, faltando)
        return None

    # Respiro entre requests para não parecer bot agressivo.
    time.sleep(random.uniform(*_SLEEP_ENTRE_REQS))

    return {
        "asin": asin,
        "titulo": titulo,
        "preco_atual": preco_atual,
        "preco_original": preco_original,
        "nota": nota,
        "total_avaliacoes": total_avaliacoes,
        "categoria": categoria,
        "imagem_url": imagem or "",
    }


# ── Orquestrador público (interface compatível com mock_api.buscar_produtos) ─

def buscar_produtos(categoria: str = "geral", limite: int = 20) -> list[dict]:
    """
    Fluxo: descobre via RSS → enriquece via scraping → fallback mock.
    Assinatura idêntica a mock_api.buscar_produtos — drop-in no pipeline.
    """
    estado = _FetchState()

    asins = descobrir_asins_via_rss(limite=limite * 2)   # descobre em excesso para compensar drops
    if not asins:
        logger.warning("Nenhum ASIN descoberto via RSS — fallback para mock.")
        from mock_api import buscar_produtos as _mock
        return _mock(categoria, limite)

    enriquecidos: list[dict] = []
    for asin in asins:
        if estado.bloqueado():
            logger.warning("Circuit breaker ativado após %d 503 — interrompendo scraping.",
                           _MAX_503_CONSECUTIVOS)
            break
        if len(enriquecidos) >= limite:
            break
        produto = enriquecer_asin(asin, estado)
        if produto:
            enriquecidos.append(produto)

    if not enriquecidos:
        logger.warning("Scraping bloqueado ou sem dados válidos — fallback para mock.")
        from mock_api import buscar_produtos as _mock
        return _mock(categoria, limite)

    logger.info("Coleta híbrida: %d produtos prontos para triagem.", len(enriquecidos))
    return enriquecidos


if __name__ == "__main__":
    produtos = buscar_produtos(limite=5)
    print(f"\n─── {len(produtos)} produtos coletados ───")
    for p in produtos:
        desc = ((p["preco_original"] - p["preco_atual"]) / p["preco_original"]) * 100
        print(f"  {p['asin']}  R$ {p['preco_atual']:>7.2f}  (-{desc:4.1f}%)  "
              f"⭐{p['nota']} [{p['total_avaliacoes']}]  {p['titulo'][:50]}")
