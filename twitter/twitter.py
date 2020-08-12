import json
import time
import utils
import requestHandler
import pandas as pd

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

    dataset = pd.read_csv('twitter/urls.csv')
    urls = dataset['url'].values

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
    start = time.time()
    perform_check()
    print(str(time.time() - start))
