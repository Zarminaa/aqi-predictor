import json

import pandas as pd

from src.features.pipeline import engineer_features
from src.supabase.supabase_client import supabase


DEFAULT_HISTORY_ROWS = 200


def load_feature_columns(path: str) -> list[str]:
    """
    Load feature column names used during training.
    """

    with open(path, "r") as f:
        return json.load(f)


def get_recent_merged_rows(
    limit: int = DEFAULT_HISTORY_ROWS,
) -> pd.DataFrame:
    """
    Fetch the most recent merged observations from Supabase.
    Returns them in chronological order.
    """

    response = (
        supabase.table("merged")
        .select("*")
        .order("datetime", desc=True)
        .limit(limit)
        .execute()
    )

    if not response.data:
        raise ValueError("Merged table is empty.")

    df = pd.DataFrame(response.data)

    df["datetime"] = pd.to_datetime(df["datetime"])

    df = (
        df.sort_values("datetime")
        .reset_index(drop=True)
    )

    return df


def build_latest_features(
    feature_columns_path: str,
    history_rows: int = DEFAULT_HISTORY_ROWS,
):
    """
    Build the latest feature vector for inference.

    Returns
    -------
    X : pd.DataFrame
        Model input.

    latest : pd.DataFrame
        Latest engineered observation.
    """

    merged = get_recent_merged_rows(history_rows)

    features = engineer_features(
        merged,
        add_target_features=False,
    )

    if features.empty:
        raise ValueError(
            "Feature engineering produced no rows."
        )

    latest = features.iloc[[-1]].copy()

    feature_columns = load_feature_columns(
        feature_columns_path
    )

    missing_features = (
        set(feature_columns)
        - set(latest.columns)
    )

    if missing_features:
        raise ValueError(
            "Missing feature columns: "
            + ", ".join(sorted(missing_features))
        )

    X = latest.loc[:, feature_columns]

    return X, latest


def predict_aqi(model, X):
    """
    Predict AQI for the next
    24, 48 and 72 hours.
    """

    prediction = model.predict(X).flatten()

    return {
        "Day 1": round(float(prediction[0]), 2),
        "Day 2": round(float(prediction[1]), 2),
        "Day 3": round(float(prediction[2]), 2),
    }