import os

BASE_URL = "https://kotodaman.jp"
NEWS_URL = "https://kotodaman.jp/info/"

EVENT_WEBHOOK = os.getenv("EVENT_WEBHOOK_URL")
GACHA_WEBHOOK = os.getenv("GACHA_WEBHOOK_URL")

USER_AGENT = {
    "User-Agent": "Mozilla/5.0"
}
