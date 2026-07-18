import pandas as pd


def add_lag_features(df: pd.DataFrame) -> pd.DataFrame:

    df = df.copy()

    lag_columns = {
        "us_aqi": [1, 3, 6, 12, 24, 48],
        "pm2_5": [1, 6, 12, 24],
        "pm10": [1, 24],
        "carbon_monoxide": [1, 24],
        "nitrogen_dioxide": [1, 24],
        "sulphur_dioxide": [1, 24],
        "ozone": [1, 24],
    }

    for column, lags in lag_columns.items():
        for lag in lags:
            df[f"{column}_lag_{lag}"] = df[column].shift(lag)

    return df