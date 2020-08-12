import auth
import pandas as pd

# Defining global variable
plane_id = ""


# Splits the world map into squares
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


# Verify squawk code
def check_squawk(item):
    global plane_id
    dataset = pd.read_csv('twitter/csv_id.csv')
    plane_ids = dataset['id'].values

    if item.get('squawk') == '7700':
        if item.get('id') not in plane_ids:
            plane_id = item.get('id')
            flight = {'id': plane_id}
            df = pd.DataFrame(flight, columns=['id'])
            df.to_csv('twitter/csv_id.csv')

            print("Tweeting...")
            tweet(item)
    pass


# Tweet the shit
def tweet(item):
    item = make_empty_check(item)
    message = "GENERAL EMERGENCY\nFlight number: " + item.get('flight') + "\nFrom " + \
        item.get('from') + " to " + item.get('to') + \
        "\nPlane type: " + \
        item.get('plane_type') + " | Registration: " + \
        item.get('plane_registration') + \
        "\nAccessible here: https://flightradar24.com/" + \
        item.get('id') + "\n #FlightEmergency #FlightRadar24"

    bot = auth.twitter_authenticate()
    bot.update_status(status=message)
    pass


# Processes data / Bullshit returned by FR24
def process_data(data):
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
                check_squawk(items)
    pass


# Checks if any field is empty, fills it if true
def make_empty_check(item):
    flight = item.get('flight')
    plane_from = item.get('from')
    plane_to = item.get('to')
    plane_type = item.get('plane_type')
    plane_registration = item.get('plane_registration')
    flight_id = item.get('id')
    registration = item.get('registration')

    if item.get('flight') == '' or item.get('flight') == None:
        flight = "N/A"
    if item.get('from') == '' or item.get('from') == None:
        plane_from = "N/A"
    if item.get('to') == '' or item.get('to') == None:
        plane_to = "N/A"
    if item.get('plane_type') == '' or item.get('plane_type') == None:
        plane_type = "N/A"
    if item.get('plane_registration') == '' or item.get('plane_registration') == None:
        plane_registration = "N/A"
    if item.get('registration') == '' or item.get('registration') == None:
        registration = "N/A"

    checked = {
        'id': flight_id,
        'squawk': item.get('squawk'),
        'registration': registration,
        'plane_type': plane_type,
        'plane_registration': plane_registration,
        'from': plane_from,
        'to': plane_to,
        'flight': flight
    }
    return checked
