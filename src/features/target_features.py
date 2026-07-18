import pandas as pd


def add_targets(df: pd.DataFrame) -> pd.DataFrame:

    df = df.copy()

    df["target_day1"] = df["us_aqi"].shift(-24)
    df["target_day2"] = df["us_aqi"].shift(-48)
    df["target_day3"] = df["us_aqi"].shift(-72)

    return df