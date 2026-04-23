#!/usr/bin/env bash
# OfertaHub — Rotina de Revisão / Saúde dos Serviços
#
# Uso:
#   ./deploy/revisao.sh           # reload + restart + status
#   ./deploy/revisao.sh --clean   # idem + limpa tabela ofertas_enviadas (re-testar envios)
#
# Premissa: serviços systemd rodam em modo --user (sem sudo).
# Se mover o projeto, ajuste PROJECT_ROOT abaixo.

set -euo pipefail

PROJECT_ROOT="/home/lukascerattiagnese/Documentos/ProjeoEmprendimento"
DB_PATH="${PROJECT_ROOT}/src/ofertahub.db"
SERVICES=(ofertahub.timer ofertahub-bot.service)

# Cores para leitura rápida no terminal
C_OK="\033[0;32m"; C_WARN="\033[0;33m"; C_ERR="\033[0;31m"; C_RST="\033[0m"
log()  { printf "${C_OK}[revisao]${C_RST} %s\n" "$*"; }
warn() { printf "${C_WARN}[revisao]${C_RST} %s\n" "$*"; }
err()  { printf "${C_ERR}[revisao]${C_RST} %s\n" "$*" >&2; }

# ── 1. Recarrega definições de unit files ─────────────────────────────────
log "Recarregando daemon do systemd (--user)…"
systemctl --user daemon-reload

# ── 2. Reinicia cada serviço da lista ─────────────────────────────────────
for svc in "${SERVICES[@]}"; do
    log "Reiniciando ${svc}…"
    if systemctl --user restart "$svc"; then
        log "  ${svc} OK"
    else
        err "  Falha ao reiniciar ${svc} — veja: journalctl --user -u ${svc} -n 50"
    fi
done

# ── 3. Limpeza opcional de histórico de envios ────────────────────────────
if [[ "${1:-}" == "--clean" ]]; then
    if [[ ! -f "$DB_PATH" ]]; then
        warn "Banco não encontrado em ${DB_PATH} — pulando limpeza."
    elif ! command -v sqlite3 >/dev/null 2>&1; then
        err "sqlite3 CLI não instalado. Instale com: sudo dnf install sqlite"
        exit 2
    else
        antes=$(sqlite3 "$DB_PATH" "SELECT COUNT(*) FROM ofertas_enviadas;")
        log "Limpando ofertas_enviadas (${antes} linhas)…"
        sqlite3 "$DB_PATH" "DELETE FROM ofertas_enviadas;"
        log "  Tabela zerada — o próximo ciclo do pipeline re-enviará todas as ofertas aprovadas."
    fi
fi

# ── 4. Status consolidado ─────────────────────────────────────────────────
echo
log "Estado atual dos serviços:"
for svc in "${SERVICES[@]}"; do
    estado=$(systemctl --user is-active "$svc" 2>/dev/null || echo "desconhecido")
    printf "  • %-32s %s\n" "$svc" "$estado"
done

echo
log "Próximo disparo do timer:"
systemctl --user list-timers ofertahub.timer --no-pager | sed -n '1,3p' || true
