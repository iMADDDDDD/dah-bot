import requests
import json
import time
import twitter
from collections import Counter
from itertools import chain

plane_id = ""


def get_coordinate(ne_lng, ne_lat, sw_lng, sw_lat, interval):
    interval = float(interval)

    n = 1 + int((ne_lng - sw_lng) / interval)
    lng_list = [
        ne_lng - (ne_lng - sw_lng) * i / n for i in range(n)]

    n = 1 + int((ne_lng - sw_lng) / interval)
    lat_list = [
        ne_lat - (ne_lat - sw_lat) * i / n for i in range(n)]

    return [
        {
            'ne_lng': vi,
            'ne_lat': vj,
            'sw_lng': lng_list[ki + 1],
            'sw_lat': lat_list[kj + 1],
            "interval": interval,
        }
        for ki, vi in enumerate(lng_list[:-1])
        for kj, vj in enumerate(lat_list[:-1])
    ]


# Makes request to the flightradar24 service
# Multithreading
def make_request(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36"}
    response = requests.get(url, headers=headers, stream=True)
    data = response.text
    data = json.loads(data)
    return data


# Verify squawk code
def check_squawk(item):
    global plane_id

    # Avoids duplicate IDs
    if plane_id == item.get('id'):
        if item.get('squawk') == '7700':
            plane_id = item.get('id')
            twitter.tweet(item)
    pass


# Process data
def process_data(data):
    for key, value in data.items():
        if not isinstance(value, int):
            if list(value)[0] != 'total':
                items = {
                    'id': key,
                    'squawk': list(value)[6],
                    'registration': list(value)[0],
                    'plane_type': list(value)[8],
                    'plane_registration': list(value)[9],
                    'from': list(value)[11],
                    'to': list(value)[12],
                    'flight': list(value)[13]
                }
                check_squawk(items)
    pass


# Checks if fields empty
def make_empty_check(item):
    flight = item.get('flight')
    plane_from = item.get('from')
    plane_to = item.get('to')
    plane_type = item.get('plane_type')
    plane_registration = item.get('plane_registration')
    flight_id = item.get('id')

    if item.get('flight') == '' or item.get('flight') == None:
        flight = "N/A"
    if item.get('from') == '' or item.get('from') == None:
        plane_from = "N/A"
    if item.get('to') == '' or item.get('to') == None:
        plane_to = "N/A"
    if item.get('plane_type') == '' or item.get('plane_type') == None:
        plane_type = "N/A"
    if item.get('plane_registration') == '' or item.get('plane_registration') == None:
        plane_registration = "N/A"
    if item.get('registration') == '' or item.get('registration') == None:
        registration = "N/A"

    checked = {
        'id': flight_id,
        'squawk': item.get('squawk'),
        'registration': registration,
        'plane_type': plane_type,
        'plane_registration': plane_registration,
        'from': plane_from,
        'to': plane_to,
        'flight': flight
    }
    return checked
