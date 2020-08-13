from flight import Flight
from handler import Handler

from concurrent.futures import ProcessPoolExecutor as PoolExecutor

import pandas as pd
import time


# Defining main function
def check_emergency():
    dataset = pd.read_csv('twitter/datasets/urls.csv')
    urls = dataset['url'].values

    handler = Handler()

    flight_id = None

    # Async requests
    with PoolExecutor(max_workers=40) as executor:
        for data in executor.map(handler.request, urls):
            for key, value in data.items():
                if isinstance(data.get(key), list):
                    if data.get(key)[6] == '7700':
                        flight = Flight(key, data.get(key)[9], data.get(key)[8],
                                        data.get(key)[11], data.get(key)[12], data.get(key)[6], data.get(key)[13])
                        handler.tweet(flight)


if __name__ == "__main__":
    while(1):
        start = time.time()
        check_emergency()
        print("[*] Took around: " + str(time.time() - start))
        time.sleep(15)
