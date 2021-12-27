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

    location_dict = requests.get(url, headers=headers, params=payload).json()

    return location_dict


def get_appointments(postal_code: str, lat: float, lng: float, service_unified_id: int) -> dict:
    ''' Get appointment data from location information '''

    today = datetime.today().strftime("%Y-%m-%d")
    end_date = (datetime.today() + relativedelta(months=4)
                ).strftime("%Y-%m-%d")
    payload = {'dateStart': today, 'dateStop': end_date, 'latitude': lat, 'longitude': lng,
               'maxDistance': 1000, 'serviceUnified': service_unified_id, 'postalCode': postal_code, 'page': 0}
    dates_url = 'https://api3.clicsante.ca/v3/availabilities'
    headers = {'accept': 'application/json, text/plain, */*', 'authorization': AUTH_STR,
               'product': 'clicsante', 'x-trimoz-role': 'public'}

    apt_request = requests.get(
        dates_url, headers=headers, params=payload)
    appointments = apt_request.json()

    return appointments


def get_establishment_services(establishment_id: int) -> list:
    ''' Get services offered by establishment '''

    url = f'https://api3.clicsante.ca/v3/establishments/{establishment_id}/services'
    payload = {'settings': True}

    headers = {'accept': 'application/json, text/plain, */*',
               'authorization': AUTH_STR, 'product': 'clicsante', 'x-trimoz-role': 'public'}

    apt_request = requests.get(url, headers=headers, params=payload)
    services = apt_request.json()

    return services


def get_first_appointment(establishment_id: int, place_id: int, establishment_unified_id: int) -> dict:
    ''' Get first available appoinment at a particular establishment, place. '''

    url = f'https://api3.clicsante.ca/v3/establishments/{establishment_id}/availabilities/first'
    payload = {'places': place_id, 'service': establishment_unified_id, 'timezone': 'America/Toronto',
               'filter1': 'undefined', 'filter2': 'undefined', 'filter3': 'undefined'}

    dates_headers = {'accept': 'application/json, text/plain, */*', 'authorization': AUTH_STR,
                     'product': 'clicsante', 'x-trimoz-role': 'public'}

    apt_request = requests.get(
        url, headers=dates_headers, params=payload)

    first_apt = apt_request.json()

    return first_apt



