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

    if category == "notice":
        return NOTICE_WEBHOOK_URL

    if category == "maintenance":
        return MAINTENANCE_WEBHOOK_URL

    return EVENT_WEBHOOK_URL


def get_color(category: str):
    category = (category or "").lower()

    if category == "gacha":
        return COLOR_GACHA

    if category == "notice":
        return COLOR_NOTICE

    if category == "maintenance":
        return COLOR_MAINTENANCE

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
):
    webhook = get_webhook(category)

    if not webhook:
        print(f"[Discord] Webhook未設定 ({category})")
        return False

    embed = {
        "title": title,
        "url": url,
        "description": description,
        "color": get_color(category),
        "footer": {
            "text": "コトダマン公式"
        }
    }

    if image:
        embed["image"] = {
            "url": image
        }

    if end_time:
        embed["fields"] = [
            {
                "name": "⏰ 終了日時",
                "value": str(end_time),
                "inline": False,
            }
        ]

    payload = {
        "embeds": [embed]
    }

    if everyone and MENTION_EVERYONE:
        payload["content"] = "@everyone"

    try:

        response = requests.post(
            webhook,
            json=payload,
            timeout=20,
        )

        if response.status_code in (200, 204):

            print(f"[Discord] 通知成功 : {title}")

            return True

        print(f"[Discord] エラー {response.status_code}")
        print(response.text)

        return False

    except Exception as e:

        print("[Discord] 通信エラー")
        print(e)

        return False