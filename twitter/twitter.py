import json
import time
import utils
import requestHandler

from concurrent.futures import ProcessPoolExecutor as PoolExecutor

# Defining global variables
Country = {
    'ne_lat': 89.000000,
    'ne_lng': 179.000000,
    'sw_lat': -89.000000,
    'sw_lng': -179.000000
}

url = "https://data-live.flightradar24.com/zones/fcgi/feed.js?bounds="
params = "&faa=1&satellite=1&mlat=1&flarm=1&adsb=1&gnd=1&air=1&vehicles=0&estimated=1&maxage=14400&gliders=1&stats=1&enc=k_l3Es3AsvJP4llucnl-vQF--32JyKB58SxmcaLb8LY"


# Checks if any flight has 7700 as squawk code
# Tweets if true
def perform_check():
    all_data = []
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

    # Async requests
    with PoolExecutor(max_workers=40) as executor:
        for data in executor.map(requestHandler.make_request, urls):
            all_data.append(data)
            pass

    # Processes on the fly
    for flight in all_data:
        processed_data = utils.process_data(flight)
    pass


if __name__ == '__main__':
    perform_check()
