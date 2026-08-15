import os
import time
import requests
import feedparser

TOKEN = os.environ["BOT_TOKEN"]
CHANNEL = os.environ["CHANNEL_ID"]

RSS_FEEDS = [
    "https://feeds.bbci.co.uk/arabic/rss.xml",
    "https://rss.nytimes.com/services/xml/rss/nyt/World.xml",
]

sent = set()

def send_news(title, link):
    text = f"📰 {title}\n\n🔗 {link}"

    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, data={
        "chat_id": CHANNEL,
        "text": text,
        "disable_web_page_preview": False
    })

while True:
    for feed_url in RSS_FEEDS:
        feed = feedparser.parse(feed_url)

        for item in feed.entries[:5]:
            link = item.get("link")
            title = item.get("title")

            if link and link not in sent:
                send_news(title, link)
                sent.add(link)

    time.sleep(30)
