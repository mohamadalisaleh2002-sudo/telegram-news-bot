import os
import requests
import feedparser

TOKEN = os.environ["BOT_TOKEN"]
CHANNEL = os.environ["CHANNEL_ID"]

RSS_FEEDS = [
    "https://feeds.bbci.co.uk/arabic/rss.xml",
    "https://rss.nytimes.com/services/xml/rss/nyt/World.xml",
]

SENT_FILE = "sent.txt"

try:
    with open(SENT_FILE, "r", encoding="utf-8") as f:
        sent = set(f.read().splitlines())
except FileNotFoundError:
    sent = set()

for feed_url in RSS_FEEDS:
    feed = feedparser.parse(feed_url)

    for item in feed.entries[:10]:
        title = item.get("title", "").strip()
        link = item.get("link", "").strip()

        if not title or not link or link in sent:
            continue

        message = f"📰 {title}\n\n🔗 {link}"

        response = requests.post(
            f"https://api.telegram.org/bot{TOKEN}/sendMessage",
            data={
                "chat_id": CHANNEL,
                "text": message,
                "disable_web_page_preview": False
            },
            timeout=15
        )

        if response.ok:
            sent.add(link)

with open(SENT_FILE, "w", encoding="utf-8") as f:
    for link in sent:
        f.write(link + "\n")
