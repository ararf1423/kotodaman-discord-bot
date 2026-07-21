from scraper import get_news_list
from parser import parse_article
from notifier import send_discord
from config import EVENT_WEBHOOK, GACHA_WEBHOOK


def main():
    news = get_news_list()

    for article in news[:5]:
        result = parse_article(article)

        print("=" * 50)
        print(result["title"])
        print(result["type"])
        print(result["end_time"])
        print(result["url"])

        # イベント
        if result["type"] == "event" and EVENT_WEBHOOK:
            send_discord(
                EVENT_WEBHOOK,
                result["title"],
                result["url"]
            )

        # ガチャ
        elif result["type"] == "gacha" and GACHA_WEBHOOK:
            send_discord(
                GACHA_WEBHOOK,
                result["title"],
                result["url"]
            )


if __name__ == "__main__":
    main()