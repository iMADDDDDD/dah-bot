import requests
import json
import time
import auth
import utils
from concurrent.futures import ProcessPoolExecutor as PoolExecutor


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
        "\nAccessible here: https://flightradar24.com/" + \
        item.get('id') + "\n #FlightEmergency #FlightRadar24"

    bot = auth.twitter_authenticate()
    bot.update_status(message)
    pass


# Performs operation check
def perform_check():
    all_data = []
    keys = []
    urls = []
    new_data = utils.get_coordinate(interval=5, **Country)
    for data in new_data:
        ne_lat = str(data.get('ne_lat')) + ","
        sw_lat = str(data.get('sw_lat')) + ","
        ne_lng = str(data.get('ne_lng')) + ","
        sw_lng = str(data.get('sw_lng'))

        bounds = ne_lat + sw_lat + ne_lng + sw_lng

        full_url = url + bounds + params
        urls.append(full_url)

    with PoolExecutor(max_workers=40) as executor:
        for data in executor.map(utils.make_request, urls):
            all_data.append(data)
            pass

    for f in all_data:
        processed_data = utils.process_data(f)
    pass


if __name__ == '__main__':
    start = time.time()
    perform_check()
    end = time.time()
    print(str(end - start))
