# src/preprocessing/validate_data.py

import pandas as pd
from pathlib import Path


DATA_PATH = Path("data/processed/lahore_merged.csv")


def validate_dataset(df):
    print("=" * 50)
    print("DATASET VALIDATION REPORT")
    print("=" * 50)

    # Basic info
    print("\nShape:")
    print(df.shape)

    print("\nColumns:")
    for col in df.columns:
        print(f"- {col}")

    # Missing values
    print("\nMissing values:")
    missing = df.isnull().sum()

    if missing.sum() == 0:
        print("✅ No missing values")
    else:
        print(missing[missing > 0])

    # Duplicate rows
    print("\nDuplicate rows:")
    duplicates = df.duplicated().sum()

    if duplicates == 0:
        print("✅ No duplicate rows")
    else:
        print(f"⚠️ {duplicates} duplicate rows")

    # Datetime checks
    print("\nDatetime validation:")

    df["datetime"] = pd.to_datetime(df["datetime"])

    print(f"Start date: {df['datetime'].min()}")
    print(f"End date:   {df['datetime'].max()}")

    # Sorted timestamps
    if df["datetime"].is_monotonic_increasing:
        print("✅ Datetime is sorted")
    else:
        print("⚠️ Datetime is not sorted")

    # Duplicate timestamps
    duplicate_times = df["datetime"].duplicated().sum()

    if duplicate_times == 0:
        print("✅ No duplicate timestamps")
    else:
        print(f"⚠️ {duplicate_times} duplicate timestamps")

    # Hourly continuity
    print("\nTime frequency check:")

    time_diff = df["datetime"].diff().value_counts()

    print(time_diff.head())

    missing_hours = (
        df["datetime"].max() - df["datetime"].min()
    ).total_seconds() / 3600 + 1

    actual_hours = len(df)

    print(
        f"\nExpected hourly records: {int(missing_hours)}"
    )
    print(
        f"Actual records: {actual_hours}"
    )

    if missing_hours == actual_hours:
        print("✅ No missing hourly timestamps")
    else:
        print(
            f"⚠️ Missing {int(missing_hours - actual_hours)} hours"
        )

    # Numerical summary
    print("\nNumerical summary:")
    print(df.describe())

    # AQI sanity check
    if "us_aqi" in df.columns:
        print("\nAQI range:")
        print(
            f"Minimum AQI: {df['us_aqi'].min()}"
        )
        print(
            f"Maximum AQI: {df['us_aqi'].max()}"
        )

        if df["us_aqi"].min() < 0:
            print("⚠️ Negative AQI detected")
        else:
            print("✅ AQI values look valid")

    print("\nValidation complete ✅")


def main():
    if not DATA_PATH.exists():
        raise FileNotFoundError(
            f"Dataset not found: {DATA_PATH}"
        )

    df = pd.read_csv(DATA_PATH)

    validate_dataset(df)


if __name__ == "__main__":
    main()