import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

from config import NEWS_URL, BASE_URL, USER_AGENT


def get_news_list():
    """
    コトダマン公式お知らせ一覧から
    記事タイトルとURLを取得する
    """

    response = requests.get(
        NEWS_URL,
        headers=USER_AGENT,
        timeout=30
    )

    response.raise_for_status()

    soup = BeautifulSoup(response.text, "lxml")

    articles = []
    seen = set()

    for a in soup.find_all("a", href=True):

        href = a["href"]

        if "/info/detail/" not in href:
            continue

        url = urljoin(BASE_URL, href)

        if url in seen:
            continue

        seen.add(url)

        title = a.get_text(" ", strip=True)

        articles.append({
            "title": title,
            "url": url
        })

    return articles
