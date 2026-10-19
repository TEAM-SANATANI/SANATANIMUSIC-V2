import asyncio

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CommandHandler, ContextTypes

from utils.downloader import search
from utils.sender import clean_error, fmt_duration


async def search_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = " ".join(context.args).strip()
    if not query:
        await update.message.reply_text("Use: /search <song name>")
        return
    status = await update.message.reply_text("🔎 Search ho raha hai...")
    try:
        results = await asyncio.to_thread(search, query, 5)
        if not results:
            await status.edit_text("Kuch nahi mila 😕")
            return
        rows = [
            [InlineKeyboardButton(f"{r['title'][:45]} ({fmt_duration(r['duration'])})",
                                  callback_data=f"dl:{r['id']}")]
            for r in results
        ]
        await status.edit_text("Ek song chuno 👇", reply_markup=InlineKeyboardMarkup(rows))
    except Exception as e:
        await status.edit_text(f"❌ Search fail: {clean_error(e)}")


def register(app):
    app.add_handler(CommandHandler(["search", "s"], search_cmd))
