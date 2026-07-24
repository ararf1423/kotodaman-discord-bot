import requests

from config import (
    EVENT_WEBHOOK_URL,
    GACHA_WEBHOOK_URL,
    NOTICE_WEBHOOK_URL,
    MAINTENANCE_WEBHOOK_URL,
    COLOR_EVENT,
    COLOR_GACHA,
    COLOR_NOTICE,
    COLOR_MAINTENANCE,
    MENTION_EVERYONE,
)


def get_webhook(category: str):
    category = (category or "").lower()

    if category == "gacha":
        return GACHA_WEBHOOK_URL

    if category == "maintenance":
        return MAINTENANCE_WEBHOOK_URL

    if category == "notice":
        return NOTICE_WEBHOOK_URL

    return EVENT_WEBHOOK_URL


def get_color(category: str):
    category = (category or "").lower()

    if category == "gacha":
        return COLOR_GACHA

    if category == "maintenance":
        return COLOR_MAINTENANCE

    if category == "notice":
        return COLOR_NOTICE

    return COLOR_EVENT


def send_discord(
    *,
    title,
    url,
    category="event",
    description="",
    image=None,
    end_time=None,
    everyone=False,
    footer="コトダマン公式",
):
    webhook = get_webhook(category)

    if not webhook:
        print(f"[Discord] Webhook未設定 ({category})")
        return

    if end_time:
        description += f"\n\n⏰ **終了日時**\n{end_time}"

    embed = {
        "title": title,
        "url": url,
        "description": description,
        "color": get_color(category),
        "footer": {
            "text": footer
        }
    }

    if image:
        embed["image"] = {
            "url": image
        }

    payload = {
        "embeds": [embed]
    }

    if everyone and MENTION_EVERYONE:
        payload["content"] = "@everyone"

    r = requests.post(webhook, json=payload)

    if r.status_code in (200, 204):
        print(f"[Discord] 通知成功 : {title}")

    else:
        print(f"[Discord] 通知失敗 {r.status_code}")
        print(r.text)