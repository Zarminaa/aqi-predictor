from pathlib import Path

import pandas as pd


def load_features():
    """
    Load engineered features dataset.
    """

    project_root = Path(__file__).resolve().parents[2]

    features_path = (
        project_root
        / "data"
        / "processed"
        / "feature_store.csv"
    )

    df = pd.read_csv(features_path)

    df["datetime"] = pd.to_datetime(df["datetime"])

    df = (
        df
        .sort_values("datetime")
        .reset_index(drop=True)
    )

    return df