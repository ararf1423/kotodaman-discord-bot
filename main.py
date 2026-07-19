from scraper import get_news_list
from parser import parse_article


def main():

    news = get_news_list()

    for article in news[:5]:

        result = parse_article(article)

        print("=" * 50)
        print(result["title"])
        print(result["type"])
        print(result["end_time"])
        print(result["url"])


if __name__ == "__main__":
    main()
