# Flight class
class Flight():

    # Instance attribute
    def __init__(self, flight_id, aircraft_id, aircraft_type, aircraft_from, aircraft_to, squawk_code, callsign):
        self.flight_id = flight_id
        self.aircraft_id = aircraft_id
        self.aircraft_type = aircraft_type
        self.aircraft_from = aircraft_from
        self.aircraft_to = aircraft_to
        self.squawk_code = squawk_code
        self.callsign = callsign

    # Duplicate setup
    def __eq__(self, value):
        return self.flight_id == value.flight_id

    pass
