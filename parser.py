import re
from datetime import datetime

from scraper import get_article


DATE_PATTERNS = [
    r"(\d{4})年(\d{1,2})月(\d{1,2})日.*?(\d{1,2}):(\d{2})",
    r"(\d{4})/(\d{1,2})/(\d{1,2}).*?(\d{1,2}):(\d{2})",
]


def parse_article(article):

    soup = get_article(article["url"])

    text = soup.get_text(" ", strip=True)

    event_type = "event"

    if "召喚" in text or "ガチャ" in text:
        event_type = "gacha"

    end_time = None

    for pattern in DATE_PATTERNS:
        m = re.search(pattern, text)

        if m:
            end_time = datetime(
                int(m.group(1)),
                int(m.group(2)),
                int(m.group(3)),
                int(m.group(4)),
                int(m.group(5))
            )
            break

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