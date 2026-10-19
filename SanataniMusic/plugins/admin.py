import asyncio

from telegram import Update
from telegram.ext import CommandHandler, ContextTypes

import config


def _is_owner(update: Update) -> bool:
    return bool(config.OWNER_ID) and update.effective_user.id == config.OWNER_ID


async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not _is_owner(update):
        return
    db = context.application.bot_data["db"]
    s = await db.stats()
    if s is None:
        await update.message.reply_text("Database off hai.")
        return
    await update.message.reply_text(
        f"📊 Users: {s['users']}\n🎵 Songs: {s['songs']}\n❤️ Favorites: {s['favs']}"
    )


async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not _is_owner(update):
        return
    db = context.application.bot_data["db"]
    if not db.enabled:
        await update.message.reply_text("Database off hai, broadcast nahi ho sakta.")
        return
    text = " ".join(context.args).strip()
    if not text:
        await update.message.reply_text("Use: /broadcast <message>")
        return
    ids = await db.all_user_ids()
    ok = fail = 0
    for uid in ids:
        try:
            await context.bot.send_message(uid, text)
            ok += 1
        except Exception:
            fail += 1
        await asyncio.sleep(0.05)  # stay under Telegram flood limits
    await update.message.reply_text(f"Done ✅ sent: {ok}, failed: {fail}")


def register(app):
    app.add_handler(CommandHandler("stats", stats))
    app.add_handler(CommandHandler("broadcast", broadcast))
