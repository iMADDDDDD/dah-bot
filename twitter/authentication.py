import os
from twython import Twython
from dotenv import load_dotenv


# Twitter authentication handler
class Authentication():

    # Authenticates the Twitter bot
    def auth(self):
        load_dotenv()

        API_KEY = os.getenv("API_KEY")
        API_SECRET_KEY = os.getenv("API_SECRET_KEY")
        ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
        ACCESS_TOKEN_SECRET = os.getenv("ACCESS_TOKEN_SECRET")

        bot = Twython(API_KEY, API_SECRET_KEY,
                      ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
        return bot
    pass
