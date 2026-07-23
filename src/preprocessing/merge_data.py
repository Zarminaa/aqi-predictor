import pandas as pd

# Read datasets
pollution = pd.read_csv("data/raw/lahore_pollution.csv")
weather = pd.read_csv("data/raw/lahore_weather.csv")

# Merge on datetime
merged = pollution.merge(weather, on="datetime", how="inner")

# Display information
print(merged.head())
print("\nData Types:")
print(merged.dtypes)
print("\nShape:", merged.shape)

# Save merged dataset
merged.to_csv("data/interim/lahore_merged.csv", index=False)

print("\nMerged dataset saved successfully!")