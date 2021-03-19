from os import getenv

COOLDOWN = getenv(
    "COOLDOWN", 1800
)  # Seconds between Tweets/Retweets, default is 1800 (30 min)
LOG_LEVEL_FILE = "INFO"
LOG_LEVEL_STDOUT = "INFO"

CONSUMER_KEY = getenv("CONSUMER_KEY", "")
CONSUMER_SECRET = getenv("CONSUMER_SECRET", "")
ACCESS_TOKEN = getenv("ACCESS_TOKEN", "")
ACCESS_SECRET = getenv("ACCESS_SECRET", "")