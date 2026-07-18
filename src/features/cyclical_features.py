import numpy as np
import pandas as pd


def add_cyclical_features(df: pd.DataFrame) -> pd.DataFrame:

    df = df.copy()

    df["hour_sin"] = np.sin(2 * np.pi * df["hour"] / 24)
    df["hour_cos"] = np.cos(2 * np.pi * df["hour"] / 24)

    df["month_sin"] = np.sin(2 * np.pi * df["month"] / 12)
    df["month_cos"] = np.cos(2 * np.pi * df["month"] / 12)

    df["dow_sin"] = np.sin(2 * np.pi * df["day_of_week"] / 7)
    df["dow_cos"] = np.cos(2 * np.pi * df["day_of_week"] / 7)

    angle = np.deg2rad(df["wind_direction_10m"])

    df["wind_dir_sin"] = np.sin(angle)
    df["wind_dir_cos"] = np.cos(angle)

    return df