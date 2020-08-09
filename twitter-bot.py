import os
from twython import Twython
from dotenv import load_dotenv

# Loading .env
load_dotenv()

API_KEY = os.getenv('API_KEY')
API_SECRET_KEY = os.getenv('API_SECRET_KEY')
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = os.getenv('ACCESS_TOKEN_SECRET')

bot = Twython(API_KEY, API_SECRET_KEY, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

"""
bounds is for setting the area you want to acquire (latitude (north), latitude (south), longitude (west), latitude (east). If not set, all data is covered.
"""
