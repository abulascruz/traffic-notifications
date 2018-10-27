import requests
import redis
import pandas as pd
from pyfcm import FCMNotification
import os

# Parameters
key_words = ['försenad', 'försening']
transport_modes = 'bus,metro,train,ship,tram'
base_url = "http://api.sl.se/api2/deviations.json"
payload = {'key': os.getenv('TRAFIKLABAPIKEY'), 'TransportMode': transport_modes}
notification_default_message = \
    "Hej, vi upptäckte förseningar på {}. Blev du påverkad? Änsök om förseningsersättning nu!"

# Request data from Trafik Lab SL Störningsinformation 2 API
response = requests.get(base_url, params=payload)
data = response.json()['ResponseData']

df_data = pd.DataFrame(data)

r = redis.from_url(url=os.getenv('REDISCLOUD_URL'))

# Filter out the traffic disturbances related to delays based on the key words
df_data = df_data[
    df_data.Details.apply(lambda detail: any(word in str.lower(detail) for word in key_words)) |
    df_data.Header.apply(lambda header: any(word in str.lower(header) for word in key_words))]

# Ensure that this delay has not been notified yet
for case_id in df_data.DevCaseGid:
    response = r.setnx(case_id, 'set')
    if not response:
        df_data = df_data[df_data.DevCaseGid != case_id]

# Replace spaces and Swedish only characters to get an acceptable topic name for FCM
df_data.Scope = df_data.Scope.apply(lambda scope: str.lower(scope))
df_data.Topic = ""
df_data.Topic = df_data.Scope.str.replace(' ', '_')
df_data.Topic = df_data.Topic.str.replace('å|ä', 'a')
df_data.Topic = df_data.Topic.str.replace('ö', 'o')

print(df_data)

# Start FCM push notification service
push_service = FCMNotification(api_key=os.getenv('FIREBASECLOUDSERVERAPI'))

# Send a new notification to each group of users registered to a given line
for index, row in df_data.iterrows():
    current_scope = df_data.Scope.at[index]
    result = push_service.notify_topic_subscribers(
        topic_name=df_data.Topic.at[index],
        message_body=notification_default_message.format(df_data.Scope.at[index])
    )
    print(notification_default_message.format(df_data.Scope.at[index]))
    print('Successfully sent message:', result)
