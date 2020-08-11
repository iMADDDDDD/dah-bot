import requests
import json


# Setting up global variable
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36"}


# Makes requests to the flightradar24 service
def make_request(url):
    response = requests.get(url, headers=headers, stream=True)
    data = response.text
    data = json.loads(data)
    return data
