import requests
import json

import pandas as pd

from flight import Flight
from authentication import Authentication

# Setting up headers
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36"}


# HTTP/Data Handler
class Handler():

    # Multiprocessing requests
    def request(self, url):
        response = requests.get(url, headers=headers, stream=True)
        data = response.text
        data = json.loads(data)
        return data

    # Tweet
    def tweet(self, data):
        auth = Authentication()
        bot = auth.auth()

        flight = self.make_empty_check(data)
        if not self.is_duplicate(flight.flight_id):
            self.make_message(flight)

            print("[!] Tweeting...")
            bot.update_status(status=message)
        else:
            print("[!] Duplicate found! Aborting")

    # Empty check
    # Checks if any field is empty, fills it if true
    def make_empty_check(self, flight):
        flight_number = flight.callsign
        plane_from = flight.aircraft_from
        plane_to = flight.aircraft_to
        plane_type = flight.aircraft_type
        flight_id = flight.flight_id
        registration = flight.aircraft_id

        if flight_number == '' or flight_number == None:
            flight_number = "N/A"
        if plane_from == '' or plane_from == None:
            plane_from = "N/A"
        if plane_to == '' or plane_to == None:
            plane_to = "N/A"
        if plane_type == '' or plane_type == None:
            plane_type = "N/A"
        if registration == '' or registration == None:
            registration = "N/A"

        flight = Flight(flight_id, registration, plane_type,
                        plane_from, plane_to, flight.squawk_code, flight_number)

        return flight

    # Handles duplicate flights
    def is_duplicate(self, flight_id):
        dataset = pd.read_csv("/root/dah-bot/twitter/datasets/flights_id.csv")

        try:
            ids = dataset['id'].values
        except:
            ids = []

        if flight_id in ids:
            return True
        else:
            df = pd.DataFrame({'id': [flight_id]}, columns=['id'])
            df.to_csv("/root/dah-bot/twitter/datasets/flights_id.csv",
                      header=False, mode='a', index=False)
            return False

    # Tweet message
    def make_message(self, flight):
        if flight.callsign == "N/A":
            message = "GENERAL EMERGENCY\nFlight number: " + str(flight.callsign) + "\nFrom " + \
                str(flight.aircraft_from) + " to " + str(flight.aircraft_to) + \
                "\nPlane type: " + \
                str(flight.aircraft_type) + " | Registration: " + \
                str(flight.aircraft_id) + \
                "\nAccessible here: https://flightradar24.com/" + str(flight.flight_id) + \
                "\n #FlightEmergency #FlightRadar24"
        else:
            message = "GENERAL EMERGENCY\nFlight number: " + str(flight.callsign) + "\nFrom " + \
                str(flight.aircraft_from) + " to " + str(flight.aircraft_to) + \
                "\nPlane type: " + \
                str(flight.aircraft_type) + " | Registration: " + \
                str(flight.aircraft_id) + \
                "\nAccessible here: https://flightradar24.com/" + \
                str(flight.callsign) + "/" + str(flight.flight_id) + \
                "\n #FlightEmergency #FlightRadar24"
