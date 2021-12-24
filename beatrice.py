import requests
import json
from datetime import datetime
from dateutil.relativedelta import relativedelta

def main():
    ''' Get available appointments from Clic-Sante '''
    
    ## Get postal code
    # postal_code = 'H3H 1K3'.replace(' ','%20')
    postal_code = 'H3H 1K3'.replace(' ','%20')

    # Get postal code location data
    url = f'https://api3.clicsante.ca/v3/geocode?address={postal_code}'
    headers = {'authority': 'api3.clicsante.ca','method': 'GET','path': f'/v3/geocode?address={postal_code}','scheme': 'https','accept': 'application/json, text/plain, */*','accept-encoding': 'gzip, deflate, br','accept-language': 'en-US,en;q=0.9','authorization': 'Basic cHVibGljQHRyaW1vei5jb206MTIzNDU2Nzgh','cookie': 'privacyConsent=1; PHPSESSID=b7b906e996ec029c2ac993890f0d0bd6','origin': 'https://portal3.clicsante.ca','product': 'clicsante','referer': 'https://portal3.clicsante.ca/','sec-fetch-dest': 'empty','sec-fetch-mode': 'cors','sec-fetch-site': 'same-site','sec-gpc': '1','user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36','x-trimoz-role': 'public',}
    location_dict = json.loads(requests.get(url,headers=headers).text)

    # Extract location data
    lat = location_dict['results'][0]['geometry']['location']['lat']
    lng = location_dict['results'][0]['geometry']['location']['lng']

    today = datetime.today().strftime("%Y-%m-%d")
    end_date = (datetime.today() + relativedelta(months=4)).strftime("%Y-%m-%d")
    dates_url = f'https://api3.clicsante.ca/v3/availabilities?dateStart={today}&dateStop={end_date}&latitude={lat}&longitude={lng}&maxDistance=1000&serviceUnified=11&postalCode={postal_code}&page=0'

    dates_headers = {'authority': 'api3.clicsante.ca','method': 'GET','path': '/v3/availabilities?dateStart=2021-12-23&dateStop=2022-04-22&latitude=45.5403219&longitude=-73.5444341&maxDistance=1000&serviceUnified=11&postalCode=H1W%202R8&page=0','scheme': 'https','accept': 'application/json, text/plain, */*','accept-encoding': 'gzip, deflate, br','accept-language': 'en-US,en;q=0.9','authorization': 'Basic cHVibGljQHRyaW1vei5jb206MTIzNDU2Nzgh','cookie': 'privacyConsent=1; PHPSESSID=b7b906e996ec029c2ac993890f0d0bd6','origin': 'https://portal3.clicsante.ca','product': 'clicsante','referer': 'https://portal3.clicsante.ca/','sec-fetch-dest':'empty','sec-fetch-mode':'cors','sec-fetch-site':'same-site','sec-gpc': '1','user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36','x-trimoz-role': 'public'}

    r = requests.get(dates_url,headers=dates_headers)
    r = json.loads(r.text)
    with open('data.json', 'w') as f:
        json.dump(r, f)

if __name__ == '__main__':
    main()