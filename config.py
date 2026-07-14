import os

RSS_FEEDS = [
    {
        "name": "The Hacker News",
        "url": "https://feeds.feedburner.com/TheHackersNews"
    },
    {
        "name": "BleepingComputer",
        "url": "https://www.bleepingcomputer.com/feed/"
    },
    {
        "name": "SecurityWeek",
        "url": "https://feeds.feedburner.com/securityweek"
    }
]

# ---------------- Database ----------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_DIR = os.path.join(BASE_DIR, "data")
os.makedirs(DATA_DIR, exist_ok=True)

DATABASE_NAME = os.path.join(DATA_DIR, "security_news.db")

# ---------------- Logging ----------------

LOG_FILE = "app.log"

REQUEST_TIMEOUT = 10