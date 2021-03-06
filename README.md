# jeopardy-bot
A Twitter bot that Tweets images of Jeopardy! questions, then answers them after a short period.

## APIs Used:
[jService API](https://jservice.io), for getting a random Jeopardy! question, along with its answer, category, value, and air date.  
[Twitter API](https://developer.twitter.com/en/docs), for posting statuses (Tweets/Retweets), and for accessing information about the bot's home timeline.

## How it works
The bot will authenticate itself with Twitter using the credentials in twitter_keys.json.

Then, the bot will start an indefinite loop as follows:

The bot will determine if a long enough time has elapsed since the last Tweet (as configured by cooldown in config.json). 
If it hasn't, the bot will wait until the cooldown has finished.

The bot will check if the most recent Tweet was a Retweet or not.

If it wasn't a Retweet it will then Retweet the most recent Tweet with the most recent answer, and continue to the next cycle.

If it was a Retweet, the bot will call the jService API for a new Jeopardy! question.

It will then turn this information into a JSON element and save it to a file, in case the bot goes offline before Retweeting the answer to a question.
The bot will generate a new image using PIL that contains the question, its category, and its value.
It will then send out this image as a Tweet, with some added information, like the date it aired.

Then, the cycle will repeat itself.

## Usage
This bot relies the Tweepy, Pillow, and pytz libraries. Install them with:
```bash
pip install Tweepy Pillow pytz
```
Make sure to fill out your Twitter credentials in the twitter_keys.json file.
After that, you can run the bot using:
```bash
python3 jeopardy_bot.py
```

## Contribution
I am always open to new ideas and suggestions. Feel free to create a PR, or contact me at connor.ford2022@gmail.com.
