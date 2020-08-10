import os

from twython import Twython
from dotenv import load_dotenv

# Loading .env
load_dotenv()

# Setting global variables
API_KEY = os.getenv("API_KEY")
API_SECRET_KEY = os.getenv("API_SECRET_KEY")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.getenv("ACCESS_TOKEN_SECRET")


# Authenticate the bot
def twitter_authenticate():
    bot = Twython(API_KEY, API_SECRET_KEY, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    return bot
