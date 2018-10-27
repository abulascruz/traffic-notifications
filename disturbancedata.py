import requests
import redis
import pandas as pd
from pyfcm import FCMNotification
import os

key_words = ['försenad', 'försening']
transport_modes = 'bus,metro,train,ship,tram'
base_url = "http://api.sl.se/api2/deviations.json"

payload = {'key': os.getenv('TRAFIKLABAPIKEY'), 'TransportMode': transport_modes}

response = requests.get(base_url, params=payload)
data = response.json()['ResponseData']

df_data = pd.DataFrame(data)

r = redis.from_url(url=os.getenv('REDISCLOUD_URL'))

df_data = df_data[
    df_data.Details.apply(lambda detail: any(word in str.lower(detail) for word in key_words)) |
    df_data.Header.apply(lambda header: any(word in str.lower(header) for word in key_words))]

for case_id in df_data.DevCaseGid:
    response = r.setnx(case_id, 'set')
    if not response:
        df_data = df_data[df_data.DevCaseGid != case_id]

print(df_data)
push_service = FCMNotification(api_key=os.getenv('FIREBASECLOUDSERVERAPI'))

for index, row in df_data.iterrows():
    result = push_service.notify_topic_subscribers(topic_name=df_data.Scope.at[index], message_body="test")
    print('Successfully sent message:', result)
