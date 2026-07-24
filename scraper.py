import requests
from bs4 import BeautifulSoup

from config import NEWS_URL, USER_AGENT

HEADERS = {
    "User-Agent": USER_AGENT
}


def get_news_list():
    """お知らせ一覧取得"""

    response = requests.get(
        NEWS_URL,
        headers=HEADERS,
        timeout=20,
    )

    response.raise_for_status()

    response.encoding = response.apparent_encoding

    soup = BeautifulSoup(response.text, "html.parser")

    news = []

    seen = set()

    for a in soup.select("a[href*='/info/detail/']"):

        title = a.get_text(strip=True)

        if not title:
            continue

        url = a.get("href", "")

        if not url:
            continue

        if not url.startswith("http"):
            url = "https://kotodaman.jp" + url

        if url in seen:
            continue

        seen.add(url)

        news.append({
            "title": title,
            "url": url
        })

    print(f"[Scraper] お知らせ取得: {len(news)}件")

    return news


def get_article(url):
    """記事取得"""

    response = requests.get(
        url,
        headers=HEADERS,
        timeout=20,
    )

    response.raise_for_status()

    response.encoding = response.apparent_encoding

    return BeautifulSoup(
        response.text,
        "html.parser"
    )