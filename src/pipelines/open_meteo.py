import requests
import pandas as pd


class WeatherClient:

    def __init__(self):
        self.base_url = "https://archive-api.open-meteo.com/v1/archive"


    def historical_weather(
        self,
        latitude,
        longitude,
        start_date,
        end_date
    ):

        params = {
            "latitude": latitude,
            "longitude": longitude,

            "start_date": start_date,
            "end_date": end_date,

            "hourly": ",".join([
                "temperature_2m",
                "relative_humidity_2m",
                "dew_point_2m",
                "surface_pressure",
                "wind_speed_10m",
                "wind_direction_10m",
                "precipitation",
                "cloud_cover"
            ]),

            "timezone": "Asia/Karachi",

            "temperature_unit": "celsius",
            "wind_speed_unit": "kmh",
            "precipitation_unit": "mm"
        }


        response = requests.get(
            self.base_url,
            params=params
        )

        print(response.url)

        response.raise_for_status()

        return response.json()



if __name__ == "__main__":

    client = WeatherClient()


    data = client.historical_weather(
        latitude=31.5204,
        longitude=74.3587,
        start_date="2020-12-01",
        end_date="2026-07-15"
    )


    hourly = data["hourly"]

    df = pd.DataFrame(hourly)

    print(df.head())

    print(df.shape)

    df.to_csv(
        "data/raw/lahore_weather.csv",
        index=False
    )

    print("Saved!")