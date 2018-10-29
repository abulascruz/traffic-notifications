# traffic-notifications
Python app deployed on Heroku to get the information regarding traffic delays in Stockholm and send them as push notifications.

## Description

The implementation of this consists of a sinle script named disturbancedata.py. This script calls the [Trafiklab SL Störningsinformation 2 API](https://www.trafiklab.se/api/sl-storningsinformation-2) every 10 minutes and filters out the data specifically related to delays. It then uses [Firebase Could Messaging](https://firebase.google.com/docs/cloud-messaging/) to send notifications to the groups of users affected by the delays on the different lines.

This project is part of the development of Spåris, an app to help you claim money back when there are delays on SL transports in Stockholm. You can find the repository for this project [here](https://github.com/Visya/sparis). 

## Set up

To install the required dependencies use:

```
pip install -r requirements.txt
```

`
