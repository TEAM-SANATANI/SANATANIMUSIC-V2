import os

try:  # .env support (useful on Termux); harmless if not installed
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

BOT_TOKEN = os.getenv("BOT_TOKEN")
MONGO_URI = os.getenv("MONGO_URI")            # optional: bot works without it
DB_NAME = os.getenv("DB_NAME", "musicbot")
OWNER_ID = int(os.getenv("OWNER_ID", "0") or 0)

MAX_SECONDS = int(os.getenv("MAX_SECONDS", "900"))   # skip songs longer than this
MAX_BYTES = 49 * 1024 * 1024                          # Telegram bot upload limit ~50 MB
MAX_PARALLEL = int(os.getenv("MAX_PARALLEL", "2"))    # simultaneous downloads (Render free = low RAM)

# Optional YouTube cookies file (Netscape format). Helps when YouTube blocks server IPs.
COOKIES_FILE = os.getenv("COOKIES_FILE", "cookies.txt")
