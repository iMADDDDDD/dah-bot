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

# Authenticate on Twitter
bot = Twython(app_key=API_KEY, app_secret=API_SECRET_KEY,
              oauth_token=ACCESS_TOKEN, oauth_token_secret=ACCESS_TOKEN_SECRET)

bot.update_status(status='Test')
