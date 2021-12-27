import requests
import json
from request_utils import get_location_data, get_appointments
from utils import postal_code_is_valid, get_service_id


def main(postal_code: str, service_id: int):
    ''' Get available appointments from Clic-Sante '''

    location_dict = get_location_data(postal_code)
    
    # Extract location data
    lat = location_dict['results'][0]['geometry']['location']['lat']
    lng = location_dict['results'][0]['geometry']['location']['lng']
        
    apt_info = get_appointments(postal_code,lat,lng,service_id)
    with open('data.json', 'w') as f:
        json.dump(apt_info, f)
    
    print(apt_info)


if __name__ == '__main__':

    postal_code = 'H1W 2R8'        
    service_id = 'covid_pcr_test'    

    if postal_code_is_valid(postal_code):
        service_id = get_service_id(service_id)
        main(postal_code, service_id)
    else:
        raise ValueError('Invalid postal code')

    
