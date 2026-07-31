# from app.dashboard.model_loader import load_model_artifacts
# from app.dashboard.predictor import build_latest_features

# from shap_analysis import SHAPAnalyzer


# FEATURE_COLUMNS_PATH = (
#     "models/aqi_xgboost_3day_/feature_columns.json"
# )


# def main():

#     model, _ = load_model_artifacts()

#     X, _ = build_latest_features(
#         FEATURE_COLUMNS_PATH,
#     )

#     analyzer = SHAPAnalyzer(
#         model,
#         X,
#     )

#     analyzer.feature_importance()

#     analyzer.summary_plot()

#     print("\nSHAP Analysis Complete!")


# if __name__ == "__main__":

#     main()

import pandas as pd

from app.training.train import load_model
from app.features.engineer import engineer_features

from analyzer import SHAPAnalyzer


df = pd.read_csv("data/interim/lahore_merged.csv")

df["datetime"] = pd.to_datetime(df["datetime"])

df = engineer_features(df)

model, _ = load_model()

X = df.drop(
    columns=[
        "target_day1",
        "target_day2",
        "target_day3",
    ]
)

analyzer = SHAPAnalyzer(
    model,
    X,
)

analyzer.feature_importance()

analyzer.summary_plot()

print("SHAP Complete!")