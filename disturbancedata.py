import requests
import datetime as dt

date_from = dt.date(2019, 10, 25)
date_to = dt.date(2018, 10, 26)
base_url = "http://api.sl.se/api2/deviations.json"
payload = {'key': 'd2b88c69767b471cb02b77d87c3d7fd6', 'TransportMode': 'bus,metro,train,ship,tram'}
response = requests.get(base_url, params=payload)

print(response.json())
