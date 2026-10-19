import time

from telegram import Update
from telegram.ext import CommandHandler, ContextTypes

HELP = (
    "🎵 Music Bot\n\n"
    "Gaane ka naam ya YouTube link bhejo (private chat me).\n\n"
    "/play <naam/link> - song download\n"
    "/search <naam> - 5 results me se chuno\n"
    "/history - pichle songs\n"
    "/favs - favorite songs\n"
    "/ping - bot check\n"
    "/id - tumhari ID\n"
    "/help - ye message"
)


def db_of(context):
    return context.application.bot_data["db"]


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await db_of(context).add_user(update.effective_user)
    name = update.effective_user.first_name if update.effective_user else "dost"
    await update.message.reply_text(f"Namaste {name}! 👋\n\n" + HELP)


async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(HELP)


async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE):
    t = time.perf_counter()
    m = await update.message.reply_text("Pong...")
    ms = int((time.perf_counter() - t) * 1000)
    db = "ON ✅" if db_of(context).enabled else "OFF ⚠️"
    await m.edit_text(f"🏓 Pong! {ms} ms\nDatabase: {db}")


async def my_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"Your ID: {update.effective_user.id}\nChat ID: {update.effective_chat.id}")


def register(app):
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(CommandHandler("ping", ping))
    app.add_handler(CommandHandler("id", my_id))
