import asyncio
import logging
import re
import shutil

from telegram import InlineKeyboardButton, InlineKeyboardMarkup

import config
from utils.downloader import download_audio

log = logging.getLogger("sender")

_sem = None


def _semaphore():
    global _sem
    if _sem is None:
        _sem = asyncio.Semaphore(config.MAX_PARALLEL)
    return _sem


def clean_error(e: Exception) -> str:
    msg = re.sub(r"\x1b\[[0-9;]*m", "", str(e))   # strip ANSI colours
    return msg.replace("ERROR:", "").strip()[:200]


def fmt_duration(sec):
    if not sec:
        return "?"
    sec = int(sec)
    return f"{sec // 60}:{sec % 60:02d}"


async def send_song(message, query: str, db, user_id: int):
    """Download `query` and reply with the audio to `message`."""
    status = await message.reply_text("🔎 Dhoondh raha hu aur download kar raha hu...")
    folder = None
    try:
        async with _semaphore():
            folder, path, info = await asyncio.to_thread(download_audio, query)

        vid = info.get("id")
        url = f"https://www.youtube.com/watch?v={vid}"
        title = info.get("title") or "Unknown"
        kb = InlineKeyboardMarkup([[InlineKeyboardButton("❤️ Favorite", callback_data=f"fav:{vid}")]])

        await message.reply_chat_action("upload_voice")
        with open(path, "rb") as f:
            await message.reply_audio(
                audio=f,
                title=title,
                performer=info.get("uploader"),
                duration=int(info.get("duration") or 0),
                reply_markup=kb,
                read_timeout=120,
                write_timeout=120,
                connect_timeout=30,
            )
        await db.add_history(user_id, title, url)
        try:
            await status.delete()
        except Exception:
            pass
    except Exception as e:
        log.warning("send_song failed: %s", e)
        try:
            await status.edit_text(f"❌ Song nahi mila: {clean_error(e)}")
        except Exception:
            pass
    finally:
        if folder:
            shutil.rmtree(folder, ignore_errors=True)
