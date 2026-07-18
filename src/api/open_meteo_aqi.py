import requests
import pandas as pd

# Lahore coordinates
LATITUDE = 31.5204
LONGITUDE = 74.3587

URL = "https://air-quality-api.open-meteo.com/v1/air-quality"

params = {
    "latitude": LATITUDE,
    "longitude": LONGITUDE,
    "start_date": "2022-08-05",
    "end_date": "2026-07-17",
    "hourly": [
        "us_aqi",
        "pm2_5",
        "pm10",
        "carbon_monoxide",
        "nitrogen_dioxide",
        "sulphur_dioxide",
        "ozone",
    ],
    "domains": "cams_global",
    "timezone": "UTC"
}

response = requests.get(URL, params=params)
response.raise_for_status()

hourly = response.json()["hourly"]
df = pd.DataFrame(hourly)

df.rename(columns={"time": "datetime"}, inplace=True)

print(df.head())
print(df.tail())
print(df.shape)

output_file = "data/raw/lahore_pollution.csv"
df.to_csv(output_file, index=False)

print(f"Saved {len(df)} rows to {output_file}")