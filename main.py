import json
from request_utils import get_first_appointment, get_location_data, get_appointments
from utils import postal_code_is_valid, get_service_unified_id, get_establishment_service_id, get_booking_link
from datetime import datetime, tzinfo
import pytz


def main(postal_code: str, service_unified_id: int):
    ''' Get available appointments from Clic-Sante '''
    
    if postal_code_is_valid(postal_code):
        postal_code = postal_code.replace(' ', '%20')
    else:
        raise ValueError('Invalid postal code')

    location_dict = get_location_data(postal_code)

    # Extract location data
    lat = location_dict['results'][0]['geometry']['location']['lat']
    lng = location_dict['results'][0]['geometry']['location']['lng']

    apt_info = get_appointments(postal_code, lat, lng, service_unified_id)
    # Now we have establishments that offer the desired service

    with open('checking2.json', 'w') as f:
        json.dump(apt_info, f)

    su_str = f'su{service_unified_id}'
    apts = []
    times = []
    for place in apt_info['places']:
        availabilities = place['availabilities'][su_str]
        if (availabilities['t07'] != 0) and (availabilities['ta7'] != 0):
            # An appointment is available
            establishment_id = place['establishment']
            place_id = place['id']
            establishment_unified_id = get_establishment_service_id(
                establishment_id, service_unified_id)
            first_apt = get_first_appointment(
                establishment_id, place_id, establishment_unified_id)

            if (first_apt is not None) and (first_apt['status'] != 404):
                time = datetime.strptime(
                    first_apt['start'], '%Y-%m-%dT%H:%M:%S+00:00')
                utc = pytz.timezone("UTC")
                time = utc.localize(time)
                time = time.astimezone(pytz.timezone('US/Eastern'))

                link = f'https://clients3.clicsante.ca/{establishment_id}/take-appt?unifiedService={service_unified_id}&portalPlace={place_id}&portalPostalCode={postal_code}&lang=en&portalServiceTemplate={establishment_unified_id}'
                first_apt['bookingLink'] = link
                first_apt['start'] = str(time)
                apts.append(first_apt)
                times.append(time)

    apts = [apt for _, apt in sorted(
        zip(times, apts), key=lambda pair: pair[0])]
    
    for apt in apts:
        start = apt['start']
        link = apt['bookingLink']
        
        print('*' * 40)
        print(f'Time: {start}')        
        print(f'Link: {link}')        


if __name__ == '__main__':

    postal_code = 'H1W 2R8'
    service_unified_id = 'blood_test'

    service_unified_id = get_service_unified_id(service_unified_id)
    main(postal_code, service_unified_id)    
