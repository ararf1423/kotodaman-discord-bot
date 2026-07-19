from scraper import get_news_list


def main():

    news = get_news_list()

    print(f"{len(news)}件取得しました")

    print()

    for article in news[:10]:

        print(article["title"])
        print(article["url"])
        print("-" * 40)


if __name__ == "__main__":
    main()
