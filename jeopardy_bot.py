import os.path
import json
import pytz
from datetime import datetime
from time import sleep
from image_creator import create_image
from jservice_api import get_question
from twitter_api import authenticate, tweet, get_last_tweet

with open("config.json") as f:
    config = json.load(f)
    # Cooldown is stored as minutes, used as seconds.
    cooldown = config["cooldown"] * 60

print("-----")
print(
    "Jeopardy Bot: a Twitter bot that automatically posts Jeopardy! questions, then answers them."
)
print("Created by Connor Ford.")

# Login to Twitter Account API
print("-----")
print("Connecting to Twitter Account API...", end="")
if authenticate():
    print("Success.")
else:
    print("Failed.")
    exit()

print("-----")
print("Loading current question from file...", end="")
with open("current_question.json") as f:
    current_question = json.load(f)
    print("Done.")

i = 0

while True:

    i += 1

    # Current time
    time_current = datetime.utcnow()

    print("-----")
    print("Iteration %s at time %s" % (i, time_current))

    print("-----")
    print("Getting last Tweet...", end="")

    # Get last Tweet
    last_tweet = get_last_tweet()

    # If it exists
    if last_tweet is not None:
        print("Success.")
    else:
        print("Failed.")
        exit()

    # Time when last Tweet was made
    time_last = datetime.strptime(
        last_tweet["created_at"], "%a %b %d %H:%M:%S %z %Y"
    ).replace(tzinfo=None)

    # Difference between current and last, in minutes
    delta = int((time_current - time_last).total_seconds())

    print("The last Tweet was posted %s seconds ago." % (delta))

    # If it has not been enough time since last tweet, wait.
    if delta < cooldown:
        remaining = cooldown - delta
        print("Waiting %s more seconds to continue." % (remaining))
        sleep(remaining)

    # If last Tweet wasn't a Retweet
    if not last_tweet["in_reply_to_status_id"]:
        print("-----")
        print("Last Tweet was not a Retweet.")

        status = (
            "Answer: "
            + current_question["answer"]
            + ". Follow @bot_jeopardy_ for more!"
        )

        print("Status: " + status)
        print("Retweeting last Tweet...", end="")
        t_response = tweet(status, id=last_tweet["id_str"])
        if t_response is not None:
            print("Success.")
            print(
                "Successfully Retweeted Tweet %s, id %s"
                % (last_tweet["id_str"], t_response["id_str"])
            )
        else:
            print("Failed.")
        continue

    print("-----")
    print("Last Tweet was a Retweet.")
    print("Grabbing jService response...", end="")

    # Get response
    j_response = get_question()

    # If it exists
    if j_response is not None:
        print("Success.")
    else:
        print("Failed.")
        exit()

    # Save as current question
    current_question["question"] = j_response[0]["question"]
    current_question["answer"] = j_response[0]["answer"]
    current_question["category"] = j_response[0]["category"]["title"]
    current_question["value"] = str(j_response[0]["value"])

    # Airdate as datetime
    airdate = datetime.strptime(j_response[0]["airdate"], "%Y-%m-%dT%H:%M:%S.%fZ")

    # Write to current_question.json
    print("-----")
    print("Saving current question to file...", end="")
    with open("current_question.json", "w") as f:
        json.dump(current_question, f)
        print("Done.")

    print("Question: " + current_question["question"])
    print("Answer: " + current_question["answer"])
    print("Category: " + current_question["category"])
    print("Value: " + current_question["value"])
    print("Date Aired: " + airdate.strftime("%Y-%m-%d"))

    print("-----")
    print("Converting question into image...", end="")

    # Image path is current datetime
    image_path = "generated/" + airdate.now().strftime("%Y_%m_%d_%H_%M_%S") + ".png"

    # Create the image
    create_image(current_question, image_path)

    # If it exists
    if os.path.isfile(image_path):
        print("Success.")
        print("Image Path: " + image_path)
    else:
        print("Failed.")
        exit()

    # Load status (Aired on {MONTH DAY, YEAR}. Category: {CATEGORY}. Follow @jeopardy_bot_ for more! )
    status = (
        "Aired on "
        + airdate.strftime("%b %d, %Y")
        + ". Category: "
        + current_question["category"].upper()
        + "."
    )

    # Send status with image
    print("Status: " + status)
    print("-----")
    print("Posting Tweet...", end="")
    t_response = tweet(status, image_path=image_path)
    if t_response is not None:
        print("Success.")
        print("Successfully sent Tweet %s." % (t_response["id"]))
    else:
        print("Failed.")
        exit()
