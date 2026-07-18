import pandas as pd

from src.features.pipeline import engineer_features


INPUT_PATH = "data/interim/lahore_merged.csv"
OUTPUT_PATH = "data/processed/feature_store.csv"


def main():

    df = pd.read_csv(INPUT_PATH)

    features = engineer_features(df)

    features.to_csv(OUTPUT_PATH, index=False)

    print("Feature engineering completed.")
    print(f"Saved to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()