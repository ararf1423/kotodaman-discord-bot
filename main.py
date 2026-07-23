from datetime import datetime, timedelta

from scraper import get_news_list
from parser import parse_article
from notifier import send_discord
from storage import load_events, save_events
from config import EVENT_WEBHOOK, GACHA_WEBHOOK


def main():

    sent = load_events()

    news = get_news_list()

    now = datetime.now()

    for article in news:

        result = parse_article(article)

        if result["end_time"] is None:
            continue

        remain = result["end_time"] - now

        if timedelta(hours=23) <= remain <= timedelta(hours=24):

            if sent.get(article["url"]):
                continue

            if result["type"] == "event":

                send_discord(
                    EVENT_WEBHOOK,
                    "⏰終了まで24時間",
                    result["url"],
                    result["end_time"],
                    result["image"]
                )

            else:

                send_discord(
                    GACHA_WEBHOOK,
                    "🎲ガチャ終了まで24時間",
                    result["url"],
                    result["end_time"],
                    result["image"]
                )

            sent[article["url"]] = True

    save_events(sent)


if __name__ == "__main__":
    main()