import json
import logging
import os.path
import sys
import pytz
import config
from datetime import datetime
from logging.handlers import TimedRotatingFileHandler
from time import sleep
from config import COOLDOWN, LOG_LEVEL_FILE, LOG_LEVEL_STDOUT
from image_creator import create_image
from jservice_api import get_question
from twitter_api import authenticate, tweet, get_last_tweet

# Init logging
formatter = logging.Formatter("[%(asctime)s] %(levelname)s - %(message)s")
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# File
if LOG_LEVEL_FILE:
    fileHandler = TimedRotatingFileHandler(
        "logs/random_discord_bot.log", when="midnight", interval=1
    )
    fileHandler.setFormatter(formatter)
    fileHandler.setLevel(LOG_LEVEL_FILE)
    logger.addHandler(fileHandler)

# Stdout
if LOG_LEVEL_STDOUT:
    consoleHandler = logging.StreamHandler(sys.stdout)
    consoleHandler.setFormatter(formatter)
    consoleHandler.setLevel(LOG_LEVEL_STDOUT)
    logger.addHandler(consoleHandler)

logger.info("Logger init.")
logger.info(f"FILE Log Level set to {LOG_LEVEL_FILE}.")
logger.info(f"STDOUT Log Level set to {LOG_LEVEL_STDOUT}.")

# Login to Twitter Account API
logger.info("Authenticating with Twitter Account API...")
if authenticate():
    logger.info("Successfully authenticated with Twitter Account API")
else:
    logger.error("Could not authenticate with Twitter Account API.")
    exit()

# Load question from file
with open("current_question.json") as f:
    current_question = json.load(f)
    logger.info("Loaded current question from file.")

i = 0

while True:

    i += 1

    # Current time
    time_current = datetime.utcnow()
    logger.info(f"Iteration {i} at time {time_current}")

    # Get last Tweet
    logger.info("Getting last Tweet...")
    last_tweet = get_last_tweet()

    # If it exists
    if last_tweet is not None:
        logger.info(f"Successfully got last Tweet. (ID {last_tweet['id_str']})")
    else:
        logger.error("Could not get last Tweet.")
        exit()

    # Time when last Tweet was made
    time_last = datetime.strptime(
        last_tweet["created_at"], "%a %b %d %H:%M:%S %z %Y"
    ).replace(tzinfo=None)

    # Difference between current and last, in minutes
    delta = int((time_current - time_last).total_seconds())

    logger.info(f"The last Tweet was posted {delta} seconds ago.")

    # If it has not been enough time since last tweet, wait.
    if delta < COOLDOWN:
        remaining = COOLDOWN - delta
        logger.info(f"Waiting {remaining} more seconds to continue.")
        sleep(remaining)

    # If last Tweet wasn't a Retweet
    if not last_tweet["in_reply_to_status_id"]:
        logger.info("Last Tweet was not a Retweet.")

        status = (
            "What is "
            + current_question["answer"]
            + "? Follow @bot_jeopardy_ for more!"
        )

        logger.debug(f"Status: {status}")
        logger.info("Retweeting last Tweet...")
        t_response = tweet(status, id=last_tweet["id_str"])
        if t_response is not None:
            logger.info(
                f"Successfully Retweeted Tweet (ID {last_tweet['id_str']}, Retweet ID {t_response['id_str']}"
            )
        else:
            logger.error(f"Was not able to Retweet Tweet (ID {last_tweet['id_str']}")
            exit()
        continue

    logger.info("Last Tweet was a Retweet.")
    logger.info("Grabbing jService response...")

    # Get response
    j_response = get_question()

    # If it exists
    if j_response is not None:
        logger.info("Successfully grabbed jService response.")
    else:
        logger.info("Could not grab jService response.")
        exit()

    # Save as current question
    current_question["question"] = j_response[0]["question"]
    current_question["answer"] = j_response[0]["answer"]
    current_question["category"] = j_response[0]["category"]["title"]
    current_question["value"] = str(j_response[0]["value"])

    logger.debug(f"Question: {current_question['question']}")
    logger.debug(f"Answer: {current_question['answer']}")
    logger.debug(f"Category: {current_question['category']}")
    logger.debug(f"Value: {current_question['value']}")
    logger.debug(f"Date Aired: {airdate.strftime('%Y-%m-%d')}")

    # Airdate as datetime
    airdate = datetime.strptime(j_response[0]["airdate"], "%Y-%m-%dT%H:%M:%S.%fZ")

    # Write to current_question.json
    logger.info("Saving current question to file...")
    with open("current_question.json", "w") as f:
        json.dump(current_question, f)
        logger.info("Successfully wrote question to file.")

    logger.info("Converting question into image...")

    # Image path is current datetime
    image_path = "generated/" + airdate.now().strftime("%Y_%m_%d_%H_%M_%S") + ".png"

    # Create the image
    create_image(current_question, image_path)

    # If it exists
    if os.path.isfile(image_path):
        logger.info("Successfully converted question into image.")
        logger.debug("Image Path: " + image_path)
    else:
        logger.error("Failed to convert question into image.")
        exit()

    # Load status (Aired on {MONTH DAY, YEAR}. Category: {CATEGORY}. Follow @jeopardy_bot_ for more! )
    status = (
        "Aired on "
        + airdate.strftime("%b %d, %Y")
        + ". Category: "
        + current_question["category"].upper()
        + ". #jeopardybot"
    )

    # Send status with image
    logger.debug(f"Status: {status}")
    logger.info("Posting Tweet...")
    t_response = tweet(status, image_path=image_path)
    if t_response is not None:
        logger.info(f"Successfully posted Tweet {t_response['id']}.")
    else:
        logger.error("Could not post Tweet.")
        exit()
