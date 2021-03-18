import config
import json
import tweepy

# Establishes connection with API
def authenticate():
    global auth
    global api

    try:
        auth = tweepy.OAuthHandler(config.consumer_key, config.consumer_secret)
        auth.set_access_token(config.access_token, config.access_secret)
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
