import pandas as pd


def add_interaction_features(df: pd.DataFrame) -> pd.DataFrame:

    df = df.copy()

    df["temp_humidity"] = (
        df["temperature_2m"]
        * df["relative_humidity_2m"]
    )

    df["wind_pm25"] = (
        df["wind_speed_10m"]
        * df["pm2_5"]
    )

    df["wind_pm10"] = (
        df["wind_speed_10m"]
        * df["pm10"]
    )

    return df