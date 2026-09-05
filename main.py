import os

import requests
from twilio.rest import Client


OWM_ENDPOINT = "https://api.openweathermap.org/data/2.5/forecast"

api_key = os.environ["OWM_API_KEY"]
account_sid = os.environ["ACCOUNT_SID"]
auth_token = os.environ["AUTH_TOKEN"]
from_number = os.environ["TWILIO_FROM_NUMBER"]
to_number = os.environ["TWILIO_TO_NUMBER"]

weather_params = {
    "lat": 23.8388,
    "lon": 78.7378,
    "appid": api_key,
    "cnt": 4,
}

response = requests.get(
    OWM_ENDPOINT,
    params=weather_params,
    timeout=30,
)
response.raise_for_status()
weather_data = response.json()

will_rain = False

for hour_data in weather_data["list"]:
    condition_code = hour_data["weather"][0]["id"]

    if condition_code < 700:
        will_rain = True

if will_rain:
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        to=to_number,
        from_=from_number,
        body="sms_appointment_reminders",
    )

    print(f"Message status: {message.status}")
else:
    print("No rain expected.")
