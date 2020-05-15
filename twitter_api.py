import tweepy, json

# Credentials
with open('twitter_keys.json') as f:
  keys = json.load(f)
  consumer_key = keys['consumer_key']
  consumer_secret = keys['consumer_secret']
  access_token = keys['access_token']
  access_secret = keys['access_secret']

# Establishes connection with API
def authenticate():
    global auth
    global api

    try:
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_secret)
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
        response = api.home_timeline(count=1)[0]
        return response
    except tweepy.TweepError:
        return None