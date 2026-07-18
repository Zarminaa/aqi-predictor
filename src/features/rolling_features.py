import pandas as pd


def add_rolling_features(df: pd.DataFrame) -> pd.DataFrame:

    df = df.copy()

    for window in [6, 12, 24]:

        df[f"aqi_mean_{window}"] = df["us_aqi"].rolling(window).mean()
        df[f"aqi_std_{window}"] = df["us_aqi"].rolling(window).std()
        df[f"aqi_min_{window}"] = df["us_aqi"].rolling(window).min()
        df[f"aqi_max_{window}"] = df["us_aqi"].rolling(window).max()

    for window in [6, 24]:

        df[f"pm25_mean_{window}"] = df["pm2_5"].rolling(window).mean()
        df[f"pm25_std_{window}"] = df["pm2_5"].rolling(window).std()

    return df