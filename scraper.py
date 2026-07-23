import requests
from bs4 import BeautifulSoup

from config import NEWS_URL, USER_AGENT


def get_news_list():
    response = requests.get(NEWS_URL, headers=USER_AGENT)

    # 文字化け対策
    response.encoding = response.apparent_encoding

    soup = BeautifulSoup(response.text, "html.parser")

    news = []

    for a in soup.select("a[href*='/info/detail/']"):
        title = a.get_text(strip=True)

        if not title:
            continue

        url = a["href"]

        if not url.startswith("http"):
            url = "https://kotodaman.jp" + url

        news.append({
            "title": title,
            "url": url
        })

    return news


def get_article(url):
    response = requests.get(url, headers=USER_AGENT)

    # ここも文字化け対策
    response.encoding = response.apparent_encoding

    return BeautifulSoup(response.text, "html.parser")