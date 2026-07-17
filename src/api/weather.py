# from src.api.client import APIClient

# class WeatherClient(APIClient):

#     def __init__(self):
#         super().__init__(
#             "https://history.openweathermap.org/data/2.5"
#         )

#     def history(self, lat, lon, start, end):

#         return self.get(
#             "history/city",
#             {
#                 "lat": lat,
#                 "lon": lon,
#                 "type": "hour",
#                 "start": start,
#                 "end": end,
#                 "units": "metric",
#             },
#         )

import requests
import os
from datetime import datetime, timezone

from dotenv import load_dotenv

# Load variables from .env
load_dotenv()

API_KEY = os.getenv("OPENWEATHER_API_KEY")


BASE_URL = "https://history.openweathermap.org/data/2.5/history/city"

lat = 31.5204
lon = 74.3587

start = int(datetime(2020, 7, 1, tzinfo=timezone.utc).timestamp())
end = int(datetime(2020, 7, 2, tzinfo=timezone.utc).timestamp())

params = {
    "lat": lat,
    "lon": lon,
    "type": "hour",
    "start": start,
    "end": end,
    "units": "metric",
    "appid": API_KEY,
}

print("Sending request...")
print()

response = requests.get(BASE_URL, params=params)

print("========== REQUEST ==========")
print("URL:")
print(response.request.url)

print("\nStatus Code:")
print(response.status_code)

print("\nHeaders:")
for key, value in response.headers.items():
    print(f"{key}: {value}")

print("\nBody:")
print(response.text)

print("\n=============================")

try:
    response.raise_for_status()
    print("\nSuccess!")
    print(response.json())
except requests.exceptions.HTTPError as e:
    print("\nHTTP Error:")
    print(e)