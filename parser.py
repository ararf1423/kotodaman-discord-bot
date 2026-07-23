import re
from datetime import datetime

from scraper import get_article


DATE_PATTERNS = [
    r"(\d{4})年(\d{1,2})月(\d{1,2})日.*?(\d{1,2}):(\d{2})",
    r"(\d{4})/(\d{1,2})/(\d{1,2}).*?(\d{1,2}):(\d{2})",
]


def find_last_datetime(text):
    dates = []

    for pattern in DATE_PATTERNS:
        for m in re.finditer(pattern, text):
            try:
                dates.append(
                    datetime(
                        int(m.group(1)),
                        int(m.group(2)),
                        int(m.group(3)),
                        int(m.group(4)),
                        int(m.group(5))
                    )
                )
            except ValueError:
                pass

    if dates:
        return max(dates)

    return None


def parse_article(article):

    soup = get_article(article["url"])

    text = soup.get_text(" ", strip=True)

    event_type = "event"

    if "召喚" in text or "ガチャ" in text:
        event_type = "gacha"

    # 一番最後の日付を終了日時として取得
    end_time = find_last_datetime(text)

    # OGP画像取得
    image = None

    og = soup.find("meta", property="og:image")

    if og:
        image = og.get("content")

    return {
        "title": article["title"],
        "url": article["url"],
        "type": event_type,
        "end_time": end_time,
        "image": image
    }