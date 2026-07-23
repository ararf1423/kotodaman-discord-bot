from datetime import datetime, timedelta

from scraper import get_news_list
from parser import parse_article
from notifier import send_discord
from storage import load_events, save_events
from config import EVENT_WEBHOOK, GACHA_WEBHOOK


def main():

    print("===== Kotodaman Notify Bot Start =====")

    sent = load_events()

    print("通知済みデータ:")
    print(sent)

    news = get_news_list()

    print(f"取得記事数: {len(news)}")

    now = datetime.now() + timedelta(hours=9)

    print(f"現在時刻: {now}")

    for article in news:

        print("\n" + "=" * 50)
        print("記事:", article["title"])
        print("URL:", article["url"])

        result = parse_article(article)

        print("種類:", result["type"])
        print("終了日時:", result["end_time"])

        if result["end_time"] is None:
            print("終了日時なし → スキップ")
            continue


        remain = result["end_time"] - now

        print("残り時間:", remain)
        print("残り時間(秒):", remain.total_seconds())


        # 23時間〜25時間以内を通知対象
        if timedelta(hours=23) <= remain <= timedelta(hours=25):

            print("✅ 通知対象")

            if sent.get(article["url"]):
                print("⚠️ すでに通知済み → スキップ")
                continue


            if result["type"] == "event":

                print("イベント通知送信")

                send_discord(
                    EVENT_WEBHOOK,
                    result["title"],
                    result["url"],
                    result["end_time"],
                    result["image"]
                )


            elif result["type"] == "gacha":

                print("ガチャ通知送信")

                send_discord(
                    GACHA_WEBHOOK,
                    result["title"],
                    result["url"],
                    result["end_time"],
                    result["image"]
                )


            sent[article["url"]] = True
            print("保存するデータ:")
            print(sent)
        else:
            print("通知対象外")


    save_events(sent)

    print("\n===== Bot Finish =====")


if __name__ == "__main__":
    main()