import requests
import time
import json


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
def make_request(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36"}
    response = requests.get(url, headers=headers)
    data = response.text
    data = json.loads(data)
    return data


if __name__ == '__main__':
    Country = {
        'ne_lat': 89.000000,
        'ne_lng': 179.000000,
        'sw_lat': -89.000000,
        'sw_lng': -179.000000
    }

    keys = []

    url = "https://data-live.flightradar24.com/zones/fcgi/feed.js?bounds="
    params = "&faa=1&satellite=1&mlat=1&flarm=1&adsb=1&gnd=1&air=1&vehicles=0&estimated=1&maxage=14400&gliders=1&stats=1&enc=k_l3Es3AsvJP4llucnl-vQF--32JyKB58SxmcaLb8LY"

    new_data = get_coordinate(interval=10, **Country)
    start = time.time()
    for data in new_data:
        ne_lat = str(data.get('ne_lat')) + ","
        sw_lat = str(data.get('sw_lat')) + ","
        ne_lng = str(data.get('ne_lng')) + ","
        sw_lng = str(data.get('sw_lng'))

        bounds = ne_lat + sw_lat + ne_lng + sw_lng

        full_url = url + bounds + params
        data = make_request(full_url)

        for key in data.keys():
            keys.append(key)

    unique_keys = set(keys)
    end = time.time()
    diff = end - start
    print(len(unique_keys))
    print(diff)
