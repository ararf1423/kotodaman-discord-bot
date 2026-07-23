from scraper import get_news_list
from parser import parse_article
from notifier import send_discord
from storage import load_events, save_events
from config import EVENT_WEBHOOK, GACHA_WEBHOOK


def main():
    sent = load_events()
    news = get_news_list()

    for article in news[:5]:

        if article["url"] in sent:
            continue

        result = parse_article(article)

        print("=" * 50)
        print(result["title"])

        if result["type"] == "event" and EVENT_WEBHOOK:
            send_discord(
                EVENT_WEBHOOK,
                result["title"],
                result["url"],
                result["end_time"],
                result["image"]
            )

        elif result["type"] == "gacha" and GACHA_WEBHOOK:
            send_discord(
                GACHA_WEBHOOK,
                result["title"],
                result["url"],
                result["end_time"],
                result["image"]
            )

        sent.append(article["url"])

    save_events(sent)


if __name__ == "__main__":
    main()