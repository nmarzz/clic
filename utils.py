import re
from typing import Union

def postal_code_is_valid(postal_code: str) -> bool:
    ''' Check if postal code is a valid postal code '''

    m = re.match(
        '[A-Z]\d[A-Z]\s\d[A-Z]\d', postal_code)

    return (m is not None)


def get_service_id(service : Union[int,str]) -> int:    
    if isinstance(service,int):
        return service
    else:
        return service_str2int(service)


def service_str2int(service : str) -> int:
    ''' Convert service string to integer '''
    if service == 'blood_test':
        return 11
    elif service == 'covid_pcr_test':
        return 236
    else:
        raise ValueError(f'Service: {service} not found')
