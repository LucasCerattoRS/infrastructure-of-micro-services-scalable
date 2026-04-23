"""
Arnês sintético de concorrência — valida que ThreadPoolExecutor acelera
_resolver_redirect em operações I/O-bound, isolando o motor de threads
da instabilidade dos feeds RSS reais.

Alvo: httpbin.org/delay/2 (resposta server-side determinística ~2s por hit).

Matemática esperada (10 alvos, 2s cada):
  Sequencial        : ~20s   (10 × 2s)
  Paralelo workers=5: ~4s    (2 ondas × 2s)
  Speedup           : ~5x

Execução:
  python tests/test_paralelo.py
"""

from __future__ import annotations

import concurrent.futures
import sys
import time
from pathlib import Path

# src/ está fora de tests/ e o projeto usa import plano (ex. "from mock_api ...").
# Injeta src/ no sys.path antes de importar _resolver_redirect.
_RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_RAIZ / "src"))

from coletor_ativo import _resolver_redirect  # noqa: E402

# 10 URLs distintas (query string diferente) para evitar qualquer cache HTTP
# intermediário e garantir que cada HEAD realmente bate em httpbin.
URLS = [f"https://httpbin.org/delay/2?id={i}" for i in range(10)]


def medir_sequencial(urls: list[str]) -> tuple[float, list[str]]:
    """Baseline: cada HEAD bloqueia o próximo. Latências somam linearmente."""
    t0 = time.perf_counter()
    resultados = [_resolver_redirect(u) for u in urls]
    return time.perf_counter() - t0, resultados


def medir_paralelo(urls: list[str], workers: int = 5) -> tuple[float, list[str]]:
    """Com pool: até `workers` HEADs em voo simultâneo. Latência ≈ onda mais lenta."""
    t0 = time.perf_counter()
    resultados: list[str] = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as pool:
        futuros = [pool.submit(_resolver_redirect, u) for u in urls]
        for futuro in concurrent.futures.as_completed(futuros):
            try:
                resultados.append(futuro.result())
            except Exception as exc:
                resultados.append(f"ERRO: {exc}")
    return time.perf_counter() - t0, resultados


def main() -> int:
    print(f"Alvo: {len(URLS)} HEAD para httpbin.org/delay/2 (~2s server-side cada)\n")

    print("[1/2] Corrida sequencial (baseline)...")
    t_seq, res_seq = medir_sequencial(URLS)
    erros_seq = sum(1 for r in res_seq if "httpbin.org" not in r)
    print(f"      Tempo : {t_seq:6.2f}s   (esperado ≈ 20s)")
    print(f"      Falhas: {erros_seq}/{len(URLS)}\n")

    print("[2/2] Corrida paralela (ThreadPoolExecutor, max_workers=5)...")
    t_par, res_par = medir_paralelo(URLS, workers=5)
    erros_par = sum(1 for r in res_par if "httpbin.org" not in str(r))
    print(f"      Tempo : {t_par:6.2f}s   (esperado ≈ 4s)")
    print(f"      Falhas: {erros_par}/{len(URLS)}\n")

    if t_par <= 0:
        print("Speedup: indeterminado (t_par = 0).")
        return 1

    speedup = t_seq / t_par
    print("─" * 48)
    print(f"Speedup medido : {speedup:5.2f}x")
    print(f"Speedup teórico: 5.00x (workers=5, 2 ondas de 5 alvos)")
    print("─" * 48)

    # Critério de aceitação: ganho mínimo de 3x prova que o pool está
    # realmente a paralelizar (margem para jitter de rede e handshake TLS).
    if speedup >= 3.0:
        print("\n✓ Motor de concorrência VALIDADO.")
        return 0
    print("\n✗ Ganho abaixo do esperado — investigar GIL / DNS / TLS handshake.")
    return 2


if __name__ == "__main__":
    sys.exit(main())
