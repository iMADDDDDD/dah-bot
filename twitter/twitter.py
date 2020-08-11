import requests
import json

import auth
import utils

Country = {
    'ne_lat': 89.000000,
    'ne_lng': 179.000000,
    'sw_lat': -89.000000,
    'sw_lng': -179.000000
}

url = "https://data-live.flightradar24.com/zones/fcgi/feed.js?bounds="
params = "&faa=1&satellite=1&mlat=1&flarm=1&adsb=1&gnd=1&air=1&vehicles=0&estimated=1&maxage=14400&gliders=1&stats=1&enc=k_l3Es3AsvJP4llucnl-vQF--32JyKB58SxmcaLb8LY"


# Tweet the shit
def tweet(item):
    item = utils.make_empty_check(item)
    message = "! General emergency !\nFlight number: " + item.get('flight') + "\nFrom " + \
        item.get('from') + " to " + item.get('to') + \
        "\nPlane type: " + \
        item.get('plane_type') + " | Registration: " + \
        item.get('plane_registration') + \
        "\nAccessible here: https://flightradar24.com/" + item.get('id')

    bot = auth.twitter_authenticate()

    print(bot.verify_credentials())
    bot.update_status(message)
    pass


# Verify squawk code
def check_squawk(data):
    for item in data:
        if item.get('squawk') == '7700':
            tweet(item)


# Performs operation
def perform_check():
    squawks = []
    new_data = utils.get_coordinate(interval=100, **Country)
    for data in new_data:
        ne_lat = str(data.get('ne_lat')) + ","
        sw_lat = str(data.get('sw_lat')) + ","
        ne_lng = str(data.get('ne_lng')) + ","
        sw_lng = str(data.get('sw_lng'))

        bounds = ne_lat + sw_lat + ne_lng + sw_lng

        full_url = url + bounds + params
        data = utils.make_request(full_url)

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
                    squawks.append(items)

    unique_squawks = [i for n, i in enumerate(
        squawks) if i not in squawks[n + 1:]]
    check_squawk(unique_squawks)
    pass


if __name__ == '__main__':
    perform_check()
