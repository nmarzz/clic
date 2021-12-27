import re
from typing import Union
from request_utils import get_establishment_services


def postal_code_is_valid(postal_code: str) -> bool:
    ''' Check if postal code is a valid postal code '''

    m = re.match(
        '[A-Z]\d[A-Z]\s\d[A-Z]\d', postal_code)

    return (m is not None)


def get_service_unified_id(service: Union[int, str]) -> int:
    if isinstance(service, int):
        return service
    else:
        return service_unified_str2int(service)


def service_unified_str2int(service: str) -> int:
    ''' Convert service string to integer '''
    if service == 'blood_test':
        return 11
    elif service == 'covid_rapid_test':
        return 236
    else:
        raise ValueError(f'Service: {service} not found')


def get_establishment_unified_id(service_unified_id: int) -> int:
    ''' Get establishment unified id. 

    Service unified id and the service id that is constant accross establishment service templates is not the same. 

    The value of service template id that is constant across establishments is the establishment unified id.    
    '''
    if service_unified_id == 11:
        return 227
    elif service_unified_id == 236:
        return 419
    else:
        raise ValueError(f'Service unified id: {service_unified_id} not found')


def get_establishment_service_id(establishment_id: int, service_unified_id: int) -> int:
    # Returns a list of services
    establishment_services = get_establishment_services(establishment_id)
    establishment_unified_id = get_establishment_unified_id(service_unified_id)
    for service in establishment_services:
        if service['service_template']['id'] == establishment_unified_id:
            return service['id']

    return -1


def get_booking_link(apointment_dict: dict) -> str:        
    pass
