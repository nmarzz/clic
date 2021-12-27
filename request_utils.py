import json
import requests
from datetime import datetime
from dateutil.relativedelta import relativedelta

AUTH_STR = 'Basic cHVibGljQHRyaW1vei5jb206MTIzNDU2Nzgh'


def get_location_data(postal_code: str) -> dict:
    ''' Get location data from postal code '''

    url = 'https://api3.clicsante.ca/v3/geocode'
    payload = {'address': postal_code}
    headers = {'accept': 'application/json, text/plain, */*',
               'authorization': AUTH_STR, 'x-trimoz-role': 'public'}

    location_dict = json.loads(requests.get(
        url, headers=headers, params=payload).text)

    return location_dict


def get_appointments(postal_code: str, lat: float, lng: float, service_id: int) -> dict:
    ''' Get appointment data from location information '''

    today = datetime.today().strftime("%Y-%m-%d")
    end_date = (datetime.today() + relativedelta(months=4)
                ).strftime("%Y-%m-%d")
    payload = {'dateStart': today, 'dateStop': end_date, 'latitude': lat, 'longitude': lng,
               'maxDistance': 1000, 'serviceUnified': service_id, 'postalCode': postal_code, 'page': 0}
    dates_url = f'https://api3.clicsante.ca/v3/availabilities'
    dates_headers = {'accept': 'application/json, text/plain, */*', 'authorization': AUTH_STR,
                     'product': 'clicsante', 'x-trimoz-role': 'public'}

    apt_request = requests.get(
        dates_url, headers=dates_headers, params=payload)
    appointments = json.loads(apt_request.text)

    return appointments
