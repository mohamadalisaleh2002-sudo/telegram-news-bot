import os
import time
import threading
import requests
import feedparser
from flask import Flask

TOKEN = os.environ["BOT_TOKEN"]
CHANNEL = os.environ["CHANNEL_ID"]

RSS_FEEDS = [
    "https://feeds.bbci.co.uk/arabic/rss.xml",
    "https://rss.nytimes.com/services/xml/rss/nyt/World.xml",
]

app = Flask(__name__)

sent = set()

@app.route("/")
def home():
    return "News bot is running!"

def send_news():
    while True:
        for feed_url in RSS_FEEDS:
            feed = feedparser.parse(feed_url)

            for item in feed.entries[:10]:
                title = item.get("title", "").strip()
                link = item.get("link", "").strip()

                if not title or not link or link in sent:
                    continue

                try:
                    response = requests.post(
                        f"https://api.telegram.org/bot{TOKEN}/sendMessage",
                        data={
                            "chat_id": CHANNEL,
                            "text": f"📰 {title}\n\n🔗 {link}",
                        },
                        timeout=15
                    )

                    if response.ok:
                        sent.add(link)

                except Exception as e:
                    print(e)

        time.sleep(30)

threading.Thread(target=send_news, daemon=True).start()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
