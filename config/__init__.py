import os
import sys
from dotenv import load_dotenv

load_dotenv()

# Support both API_TOKEN and BOT_TOKEN in .env
BOT_TOKEN = os.getenv("BOT_TOKEN") or os.getenv("API_TOKEN")
if not BOT_TOKEN:
    print("Error: Set BOT_TOKEN or API_TOKEN in .env", file=sys.stderr)
    sys.exit(1)

_admin_raw = os.getenv("ADMIN_CHAT_IDS") or os.getenv("ADMIN_CHAT_ID")
if not _admin_raw:
    print("Error: Set ADMIN_CHAT_IDS in .env (comma-separated Telegram chat IDs)", file=sys.stderr)
    sys.exit(1)
ADMIN_CHAT_IDS: list[int] = [int(x.strip()) for x in _admin_raw.split(",") if x.strip()]
