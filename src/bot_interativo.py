"""
OfertaHub — Bot Interativo (processo contínuo)
Escuta comandos dos usuários via Telegram polling e gerencia assinaturas no SQLite.

Comandos disponíveis:
  /start            — cadastro e boas-vindas
  /filtros          — teclado inline para selecionar categorias de interesse
  /minhas_categorias — lista as categorias ativas do usuário
  /cancelar         — remove todas as assinaturas
"""

import logging
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
)

import db
from config import CATEGORIAS_DISPONIVEIS, TELEGRAM_TOKEN

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [BOT] %(message)s",
)
logger = logging.getLogger("bot_interativo")


# ── Teclado dinâmico ───────────────────────────────────────────────────────

def _keyboard_filtros(categorias_ativas: list[str]) -> InlineKeyboardMarkup:
    """
    Gera o teclado inline com todas as categorias disponíveis.
    Categorias assinadas exibem ✅; as demais exibem ⬜.
    Layout: 2 colunas.
    """
    botoes, linha = [], []
    for cat in CATEGORIAS_DISPONIVEIS:
        icone = "✅" if cat in categorias_ativas else "⬜"
        linha.append(InlineKeyboardButton(f"{icone} {cat}", callback_data=f"filtro:{cat}"))
        if len(linha) == 2:
            botoes.append(linha)
            linha = []
    if linha:
        botoes.append(linha)
    return InlineKeyboardMarkup(botoes)


def _texto_filtros(categorias_ativas: list[str]) -> str:
    if categorias_ativas:
        lista = "\n".join(f"  ✅ {c}" for c in categorias_ativas)
        return f"🎯 *Suas categorias ativas:*\n{lista}\n\nToque para ativar ou desativar\\."
    return "🎯 Nenhuma categoria ativa\\. Toque para escolher o que quer receber\\."


# ── Handlers de comandos ───────────────────────────────────────────────────

async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    db.upsert_user(user.id, user.full_name)
    logger.info("/start: %s (%d)", user.full_name, user.id)

    await update.message.reply_text(
        f"👋 Olá, *{user.first_name}*\\! Bem\\-vindo ao *OfertaHub*\\.\n\n"
        "Sou seu caçador de ofertas pessoal 🤖\n\n"
        "Use /filtros para escolher as categorias que te interessam e começar a "
        "receber alertas direto aqui\\.",
        parse_mode="MarkdownV2",
    )


async def cmd_filtros(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    db.upsert_user(user.id, user.full_name)
    categorias_ativas = db.get_categorias_user(user.id)

    await update.message.reply_text(
        text=_texto_filtros(categorias_ativas),
        parse_mode="MarkdownV2",
        reply_markup=_keyboard_filtros(categorias_ativas),
    )


async def cmd_minhas_categorias(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    categorias = db.get_categorias_user(update.effective_user.id)
    if not categorias:
        await update.message.reply_text(
            "Você ainda não assinou nenhuma categoria\\. Use /filtros para escolher\\.",
            parse_mode="MarkdownV2",
        )
        return

    lista = "\n".join(f"  • {c}" for c in categorias)
    await update.message.reply_text(
        f"📋 *Suas assinaturas ativas:*\n{lista}",
        parse_mode="MarkdownV2",
    )


async def cmd_cancelar(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    db.limpar_categorias(update.effective_user.id)
    await update.message.reply_text(
        "✅ Todas as suas assinaturas foram removidas\\.\n"
        "Use /filtros para reconfigurar quando quiser\\.",
        parse_mode="MarkdownV2",
    )
    logger.info("/cancelar: %d limpou todas as categorias", update.effective_user.id)


# ── Handler de callback (clique nos botões) ────────────────────────────────

async def cb_filtro(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()   # remove o "spinner" do botão imediatamente

    _, categoria = query.data.split(":", 1)
    user_id = query.from_user.id

    categorias_ativas = db.toggle_categoria(user_id, categoria)
    logger.info("Toggle '%s' para user %d → ativas: %s", categoria, user_id, categorias_ativas)

    # Edita a mensagem original com o teclado atualizado (sem reenviar)
    await query.edit_message_text(
        text=_texto_filtros(categorias_ativas),
        parse_mode="MarkdownV2",
        reply_markup=_keyboard_filtros(categorias_ativas),
    )


# ── Entrypoint ─────────────────────────────────────────────────────────────

def main() -> None:
    db.inicializar_banco()
    logger.info("Banco de dados inicializado.")

    app = Application.builder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start",              cmd_start))
    app.add_handler(CommandHandler("filtros",            cmd_filtros))
    app.add_handler(CommandHandler("minhas_categorias",  cmd_minhas_categorias))
    app.add_handler(CommandHandler("cancelar",           cmd_cancelar))
    app.add_handler(CallbackQueryHandler(cb_filtro, pattern=r"^filtro:"))

    logger.info("Bot iniciado — aguardando mensagens...")
    app.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    main()
