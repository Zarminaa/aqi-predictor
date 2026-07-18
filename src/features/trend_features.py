import pandas as pd


def add_trend_features(df: pd.DataFrame) -> pd.DataFrame:

    df = df.copy()

    df["aqi_change"] = df["us_aqi"].diff()
    df["pm25_change"] = df["pm2_5"].diff()
    df["temperature_change"] = df["temperature_2m"].diff()
    df["pressure_change"] = df["surface_pressure"].diff()

    return df