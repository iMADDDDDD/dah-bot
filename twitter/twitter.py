import json
import time
import utils
import requestHandler
import pandas as pd

from concurrent.futures import ProcessPoolExecutor as PoolExecutor


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
