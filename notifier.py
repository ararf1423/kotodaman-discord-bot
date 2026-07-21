import requests


def send_discord(webhook_url, title, url):
    embed = {
        "title": title,
        "url": url,
        "color": 0x00B0F4
    }

    requests.post(
        webhook_url,
        json={
            "embeds": [embed]
        },
        timeout=20
    )