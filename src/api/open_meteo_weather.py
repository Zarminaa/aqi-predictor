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

            "timezone": "UTC",

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
        start_date="2022-08-05",
        end_date="2026-07-22"
    )

    hourly = data["hourly"]

    df = pd.DataFrame(hourly)

    # Rename "time" to "datetime" to match the database schema
    df.rename(columns={"time": "datetime"}, inplace=True)

    # Convert datetime to PostgreSQL-friendly format
    df["datetime"] = (
        pd.to_datetime(df["datetime"])
        .dt.strftime("%Y-%m-%d %H:%M:%S")
    )

    # Ensure integer columns are integers
    integer_columns = [
        "relative_humidity_2m",
        "wind_direction_10m",
        "cloud_cover"
    ]

    for column in integer_columns:
        df[column] = df[column].astype("Int64")

    print(df.head())
    print(df.dtypes)
    print(df.shape)

    df.to_csv(
        "data/raw/lahore_weather.csv",
        index=False
    )

    print("Saved!")