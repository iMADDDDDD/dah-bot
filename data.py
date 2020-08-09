import requests
import json


def search_request(param):
    url = "https://www.flightradar24.com/v1/search/web/"
    query = "find?query=" + str(param) + "&limit=20"
    data = make_request(url + query)
    flights = parse_data(data)
    return flights


# Makes request to the flightradar24 service
def make_request(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36"}
    response = requests.get(url, headers=headers)
    data = response.text
    data = json.loads(data)
    return data


# Parses data into a list
def parse_data(data):
    flight_list = []
    for flight in data['results']:
        if flight.get('id')[0].isdigit():
            flight_data = {
                'callsign': flight['detail'].get('callsign'),
                'from': flight['detail'].get('schd_from'),
                'to': flight['detail'].get('schd_to'),
                'plane': flight['detail'].get('ac_type'),
                'plane_type': flight['detail'].get('reg')
            }
            flight_list.append(flight_data)
    return flight_list
