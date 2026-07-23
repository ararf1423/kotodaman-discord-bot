import requests


def send_discord(webhook_url, title, url):
    embed = {
        "title": title,
        "url": url,
        "color": 0x00B0F4
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