import json
import pandas as pd

from app.dashboard.model_loader import load_model_artifacts
from src.explainability.shap_analysis import SHAPAnalyzer


def main():

    model, _ = load_model_artifacts()

    df = pd.read_csv("data/processed/features.csv")

    with open("models/aqi_xgboost_3day_/feature_columns.json") as f:
        feature_columns = json.load(f)

    X = df[feature_columns]

    analyzer = SHAPAnalyzer(
        model=model,
        X=X,
    )

    analyzer.feature_importance()
    analyzer.summary_plot()

    print("\nSHAP Analysis Complete!")


if __name__ == "__main__":
    main()