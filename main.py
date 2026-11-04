import requests
import smtplib
import os

OWM_API_KEY = os.environ.get("OWM_API_KEY")
OWM_API_ENDPOINT = "https://api.openweathermap.org/data/2.5/forecast"

EMAIL = os.environ.get("EMAIL_ADDR")
EMAIL_PASSWORD = os.environ.get("EMAIL_PW")

parameters = {
    "lat": "-9.467070",
    "lon": "147.196030",
    "appid": OWM_API_KEY,
    "cnt": 4,
}

response = requests.get(url=OWM_API_ENDPOINT, params= parameters)
response.raise_for_status()

data = response.json()

# print(data["list"])

weather_updates = data["list"]

rain_detected_count = 0
for forecast in weather_updates:
    if forecast["weather"][0]["id"] < 700:
        rain_detected_count += 1

if rain_detected_count > 0:
    with smtplib.SMTP(host="smtp.gmail.com", port=587) as connection:
        connection.starttls()
        connection.login(user=EMAIL, password=EMAIL_PASSWORD)
        connection.sendmail(from_addr=EMAIL, to_addrs=EMAIL, msg="Subject: ALERT!\n"
                                                                 "Rain is forecast for today, don't forget your umbrella!")
