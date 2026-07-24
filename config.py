import os

# ===========================
# 基本設定
# ===========================

BASE_URL = "https://kotodaman.jp"
NEWS_URL = f"{BASE_URL}/info/#news-list-area"

USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/137.0.0.0 Safari/537.36"
)

# ===========================
# Discord Webhook
# ===========================

EVENT_WEBHOOK_URL = os.getenv("EVENT_WEBHOOK_URL")
GACHA_WEBHOOK_URL = os.getenv("GACHA_WEBHOOK_URL")
NOTICE_WEBHOOK_URL = os.getenv("NOTICE_WEBHOOK_URL")
MAINTENANCE_WEBHOOK_URL = os.getenv("MAINTENANCE_WEBHOOK_URL")

# ===========================
# 通知設定
# ===========================

CHECK_INTERVAL_MINUTES = 10

# 24時間前通知で everyone を付ける
MENTION_EVERYONE = True

# Embedカラー
COLOR_EVENT = 0x2ECC71        # 緑
COLOR_GACHA = 0xF1C40F        # 黄
COLOR_NOTICE = 0x3498DB       # 青
COLOR_MAINTENANCE = 0xE74C3C  # 赤

# ===========================
# 保存ファイル
# ===========================

EVENTS_FILE = "events.json"
SEEN_NEWS_FILE = "seen_news.json"