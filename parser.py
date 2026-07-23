import re
from datetime import datetime

from scraper import get_article


DATE_PATTERNS = [
    r"(\d{4})年(\d{1,2})月(\d{1,2})日.*?(\d{1,2}):(\d{2})",
    r"(\d{4})/(\d{1,2})/(\d{1,2}).*?(\d{1,2}):(\d{2})",
]


def to_datetime(match):
    return datetime(
        int(match.group(1)),
        int(match.group(2)),
        int(match.group(3)),
        int(match.group(4)),
        int(match.group(5))
    )


def find_end_datetime(text):
    """
    終了日時をできるだけ正確に取得する
    """

    priority_keywords = [
        "終了",
        "終了日時",
        "終了予定",
        "開催期間",
        "開催日時",
        "まで",
        "15:59",
        "23:59"
    ]

    # キーワード付近の日付を優先
    for keyword in priority_keywords:

        pos = text.find(keyword)

        if pos == -1:
            continue

        target = text[pos:pos + 400]

        for pattern in DATE_PATTERNS:
            m = re.search(pattern, target)

            if m:
                return to_datetime(m)

    # 見つからなければ最後の日付
    dates = []

    for pattern in DATE_PATTERNS:
        for m in re.finditer(pattern, text):
            try:
                dates.append(to_datetime(m))
            except:
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

    end_time = find_end_datetime(text)

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