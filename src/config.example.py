# OfertaHub — Template de Configuração
# Copie este arquivo para `config.py` e preencha os valores antes de rodar o sistema.
#
#     cp config.example.py config.py
#
# `config.py` é ignorado pelo Git — mantém tokens fora do repositório.

# ── Pré-filtros mínimos (rejeição rápida antes do Score) ──────────────────
FILTRO = {
    "desconto_minimo_pct": 20.0,   # % de desconto mínimo aceito
    "nota_minima":         4.0,    # nota mínima (0–5)
    "avaliacoes_minimas":  50,     # volume mínimo para a nota ser confiável
    "preco_maximo":        None,   # BRL; None = sem limite global
}

# ── Fórmula: Score = (Wp*P) + (Wa*A) + (Wv*log10(V)) - C_penalidade ─────
SCORE_PESOS = {
    "Wp": 40,   # peso do desconto  (0–40 pts)
    "Wa": 40,   # peso da avaliação (0–40 pts)
    "Wv":  4,   # coeficiente do volume; 4 × log10(100k=5) = 20 pts máx
}

PENALIDADES = {
    "volatilidade_alta":      8,   # preço oscilou > 30% no histórico
    "historico_insuficiente": 3,   # < 3 registros no histórico
}

# ── Blacklist ─────────────────────────────────────────────────────────────
BLACKLIST = {
    "marcas_bloqueadas":     ["genérico", "sem marca", "noname"],
    "categorias_bloqueadas": [],
}

# ── Categorias disponíveis para assinatura no bot ─────────────────────────
CATEGORIAS_DISPONIVEIS = [
    "Eletrônicos", "Áudio",        "Periféricos",   "Monitores",
    "E-readers",   "Eletrodomésticos", "Bolsas",    "Segurança",
    "Casa & Jardim", "Esportes",   "Livros",        "Moda",
]

# ── Amazon Product Advertising API v5 ────────────────────────────────────
# Obtenha suas credenciais em: https://affiliate-program.amazon.com.br/
AMAZON_API = {
    "access_key":  "",   # PREENCHA
    "secret_key":  "",   # PREENCHA
    "partner_tag": "",   # PREENCHA  ex: "ofertahub0f0-20"
    "region":      "us-east-1",
}

AFFILIATE_TAG = AMAZON_API["partner_tag"] or "ofertahub0f0-20"

# ── Telegram ──────────────────────────────────────────────────────────────
# Crie um bot com @BotFather e cole o token aqui.
TELEGRAM_TOKEN = ""   # PREENCHA  ex: "1234567890:ABC-DEF1234ghIkl-zyx57W2v1u123ew11"
