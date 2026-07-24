from datetime import datetime, timedelta

from scraper import get_news_list
from parser import parse_article
from notifier import send_discord
from storage import (
    load_events,
    save_events,
    load_seen_news,
    save_seen_news,
)

def main():

    print("===== Kotodaman Notify Bot Ver2 =====")

    sent_events = load_events()
    seen_news = load_seen_news()

    news = get_news_list()

    print(f"取得記事数: {len(news)}")

    # JST
    now = datetime.utcnow() + timedelta(hours=9)

    print("現在:", now)

    # ==========================
    # 初回起動
    # ==========================

    if len(seen_news) == 0:

        print("初回起動")

        for article in news:
            seen_news.append(article["url"])

        save_seen_news(seen_news)

        print("最新記事を保存しました。通知は行いません。")

    else:

        print("新着記事チェック開始")

        # 古い→新しい順で通知したいので逆順
        for article in reversed(news):

            if article["url"] in seen_news:
                continue

            print("新着:", article["title"])

            result = parse_article(article)

            desc = ""

            if result["published"]:
                desc += f"📅 公開日\n{result['published']}\n"

            send_discord(
                title="🆕 新しいお知らせ",
                url=result["url"],
                category=result["type"],
                description=f"{result['title']}\n\n{desc}",
                image=result["image"],
                everyone=False,
            )

            seen_news.append(article["url"])

        save_seen_news(seen_news)

    print("新着チェック終了")

    # ==========================
    # 24時間前通知
    # ==========================

    print("24時間通知チェック")

    for article in news:

        result = parse_article(article)

        if result["end_time"] is None:
            continue

        remain = result["end_time"] - now

        print(
            result["title"],
            remain,
        )

        if not (
            timedelta(hours=23)
            <= remain
            <= timedelta(hours=25)
        ):
            continue

        url = result["url"]

        if sent_events.get(url):

            print("通知済み")

            continue

        description = (
            f"📢 {result['title']}\n\n"
        )

        if result["published"]:
            description += (
                f"📅 公開日\n"
                f"{result['published']}\n\n"
            )

        description += (
            f"🔗 {result['url']}"
        )
        send_discord(
            title="⏰ あと24時間で終了！",
            url=result["url"],
            category=result["type"],
            description=description,
            image=result["image"],
            end_time=result["end_time"].strftime("%Y年%m月%d日 %H:%M"),
            everyone=True,
        )

        sent_events[url] = True

        save_events(sent_events)

        print("24時間通知送信:", result["title"])

    print("24時間通知チェック終了")

    print("===== Bot Finish =====")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        import traceback

        print("===== ERROR =====")
        print(e)
        traceback.print_exc()