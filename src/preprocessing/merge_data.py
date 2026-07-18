import pandas as pd

# Read datasets
pollution = pd.read_csv("data/raw/lahore_pollution.csv")
weather = pd.read_csv("data/raw/lahore_weather.csv")

# Rename weather timestamp column
weather.rename(columns={"time": "datetime"}, inplace=True)

# Convert timestamps to datetime objects
pollution["datetime"] = pd.to_datetime(pollution["datetime"])
weather["datetime"] = pd.to_datetime(weather["datetime"])

# Merge on datetime
merged = pollution.merge(weather, on="datetime", how="inner")

# Display information
print(merged.head())
print("\nShape:", merged.shape)

# Save merged dataset
merged.to_csv("data/interim/lahore_merged.csv", index=False)

print("\nMerged dataset saved successfully!")