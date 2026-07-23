import requests


def send_discord(webhook_url, title, url, end_time=None, image=None):

    description = ""

    if end_time:
        description += f"⏰ **終了日時**\n{end_time.strftime('%Y/%m/%d %H:%M')}\n\n"

    description += f"🔗 {url}"

    embed = {
        "title": title,
        "description": description,
        "url": url,
        "color": 0x00B0F4
    }

    if image:
        embed["image"] = {
            "url": image
        }

    response = requests.post(
        webhook_url,
        json={
            "embeds": [embed]
        },
        timeout=20
    )

    print(f"Discord Status: {response.status_code}")
    print(response.text)