import json
import os
import pandas as pd


def load_feature_columns(path):

    with open(path, "r") as f:
        return json.load(f)



def get_latest_features(feature_view, feature_columns_path):

    # Get all feature data
    df = feature_view.get_batch_data()

    print("Feature data shape:", df.shape)

    # Sort by timestamp if available
    if "timestamp" in df.columns:
        df = df.sort_values("timestamp")


    # Take latest row
    latest = df.tail(1)


    feature_columns = load_feature_columns(
        feature_columns_path
    )


    X = latest[feature_columns]


    return X

def predict_aqi(model, X):

    prediction = model.predict(X)

    prediction = prediction.flatten()

    return {
        "Day 1": round(float(prediction[0]), 2),
        "Day 2": round(float(prediction[1]), 2),
        "Day 3": round(float(prediction[2]), 2),
    }

