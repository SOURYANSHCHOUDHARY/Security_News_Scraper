import feedparser
import requests
from bs4 import BeautifulSoup

from config import RSS_FEEDS, REQUEST_TIMEOUT


def get_articles():

    articles = []

    for feed in RSS_FEEDS:

        print(f"Fetching: {feed['name']}")

        rss = feedparser.parse(feed["url"])

        for entry in rss.entries:

            articles.append({
                "source": feed["name"],
                "title": entry.title,
                "link": entry.link,
                "published": entry.get("published", "Unknown")
            })

    return articles


def get_article_text(url):

    try:
        response = requests.get(url, timeout=REQUEST_TIMEOUT)

        soup = BeautifulSoup(response.text, "html.parser")

        paragraphs = soup.find_all("p")

        text = " ".join(p.get_text() for p in paragraphs)

        return text

    except Exception as e:
        print(f"Error downloading {url}: {e}")
        return ""