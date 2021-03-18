from os import getenv

cooldown = getenv("cooldown", 1800)  # Seconds between Tweets/Retweets, default is 1800 (30 min)
consumer_key = getenv("consumer_key", "")
consumer_secret = getenv("consumer_secret", "")
access_token = getenv("access_token", "")
access_secret = getenv("access_secret", "")