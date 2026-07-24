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
        int(match.group(5)),
    )


def find_end_datetime(text):
    priority_keywords = [
        "終了日時",
        "終了予定",
        "終了",
        "開催期間",
        "開催日時",
        "まで",
    ]

    for keyword in priority_keywords:

        pos = text.find(keyword)

        if pos == -1:
            continue

        target = text[pos:pos + 500]

        for pattern in DATE_PATTERNS:
            m = re.search(pattern, target)

            if m:
                return to_datetime(m)

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


def classify_article(title, text):

    target = f"{title} {text}".lower()

    gacha = [
        "召喚",
        "ガチャ",
        "ピックアップ",
        "ステップアップ",
    ]

    maintenance = [
        "メンテ",
        "メンテナンス",
        "障害",
        "不具合",
        "不具合修正",
        "緊急",
    ]

    notice = [
        "キャンペーン",
        "プレゼント",
        "配布",
        "生放送",
        "アップデート",
        "更新",
        "お知らせ",
    ]

    for word in gacha:
        if word.lower() in target:
            return "gacha"

    for word in maintenance:
        if word.lower() in target:
            return "maintenance"

    for word in notice:
        if word.lower() in target:
            return "notice"

    return "event"


def parse_article(article):

    soup = get_article(article["url"])

    text = soup.get_text(" ", strip=True)

    title = article["title"]

    category = classify_article(title, text)

    end_time = find_end_datetime(text)

    image = None

    og = soup.find("meta", property="og:image")

    if og:
        image = og.get("content")

    published = None

    time_tag = soup.find("time")

    if time_tag:

        published = (
            time_tag.get("datetime")
            or time_tag.get_text(strip=True)
        )

    return {
        "title": title,
        "url": article["url"],
        "type": category,
        "end_time": end_time,
        "image": image,
        "published": published,
    }