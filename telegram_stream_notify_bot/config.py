import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_IDS = [int(id) for id in os.getenv("ADMIN_IDS", "").split(",") if id]

# Добавляем настройки прокси
PROXY_URL = os.getenv("PROXY_URL")  # например: socks5://127.0.0.1:9150 или http://proxy:8080
PROXY_TYPE = os.getenv("PROXY_TYPE", "http")  # http, socks5

TWITCH_CLIENT_ID = os.getenv("TWITCH_CLIENT_ID")
TWITCH_CLIENT_SECRET = os.getenv("TWITCH_CLIENT_SECRET")
TWITCH_REDIRECT_URI = os.getenv("TWITCH_REDIRECT_URI")

VK_CLIENT_ID = os.getenv("VK_CLIENT_ID")
VK_CLIENT_SECRET = os.getenv("VK_CLIENT_SECRET")
VK_REDIRECT_URI = os.getenv("VK_REDIRECT_URI")
VK_POLL_INTERVAL = 30

WEBHOOK_BASE_URL = os.getenv("WEBHOOK_BASE_URL")
WEBHOOK_PORT = int(os.getenv("WEBHOOK_PORT", 8080))

PAYMENT_API_KEY = os.getenv("PAYMENT_API_KEY")
PAYMENT_WEBHOOK_SECRET = os.getenv("PAYMENT_WEBHOOK_SECRET")

DB_PATH = "Data/bot.db"
DEFAULT_TEMPLATE = "✨ {channel} начал стрим на {platform}!\n🎮 {title}\n👉 {url}"

DEFAULT_COOLDOWN_FREE = {
    "stream_start": 0,
    "stream_end": 0,
    "title_change": 60,
    "category_change": 60
}

ALLOWED_COOLDOWNS = [0, 1, 5, 10, 15, 30, 60, 180, 360, 720, 1440]
MAX_COOLDOWN = 10080