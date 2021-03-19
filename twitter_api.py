import config
import json
import tweepy
from config import CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_SECRET

# Establishes connection with API
def authenticate():
    global auth
    global api

    try:
        auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
        api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())
        return True
    except tweepy.TweepError:
        return False


# POSTS a status with a specified image
def tweet(status, image_path=None, id=None):
    try:
        if image_path is not None:
            response = api.update_with_media(image_path, status)
        else:
            response = api.update_status(status, in_reply_to_status_id=id)
        return response
    except tweepy.TweepError as e:
        print(e)
        return None


# Gets last tweet in Home Timeline (not updated live)
def get_last_tweet():
    try:
        response = api.user_timeline()[0]
        return response
    except tweepy.TweepError:
        return None
