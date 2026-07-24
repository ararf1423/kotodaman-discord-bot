import json
import os
from config import EVENTS_FILE, SEEN_NEWS_FILE


def _load_json(path, default):
    """JSONを安全に読み込む"""
    try:
        if not os.path.exists(path):
            return default

        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    except Exception as e:
        print(f"[Storage] {path} 読み込み失敗: {e}")
        return default


def _save_json(path, data):
    """JSONを安全に保存する"""
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(
                data,
                f,
                ensure_ascii=False,
                indent=2,
            )

    except Exception as e:
        print(f"[Storage] {path} 保存失敗: {e}")


# ==========================
# イベント管理
# ==========================

def load_events():
    return _load_json(EVENTS_FILE, {})


def save_events(events):
    _save_json(EVENTS_FILE, events)


# ==========================
# 新着記事管理
# ==========================

def load_seen_news():
    return _load_json(SEEN_NEWS_FILE, [])


def save_seen_news(news):
    _save_json(SEEN_NEWS_FILE, news)


def has_seen(url):
    return url in load_seen_news()


def add_seen(url):
    news = load_seen_news()

    if url not in news:
        news.append(url)

    save_seen_news(news)