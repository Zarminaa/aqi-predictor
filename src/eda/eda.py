import os
import pandas as pd
import matplotlib.pyplot as plt

# ----------------------------
# Load Data
# ----------------------------

df = pd.read_csv("data/processed/lahore_merged.csv")

df["datetime"] = pd.to_datetime(df["datetime"])

# ----------------------------
# Create plots folder
# ----------------------------

os.makedirs("src/eda/plots", exist_ok=True)

# ----------------------------
# Dataset Overview
# ----------------------------

print("=" * 50)
print("DATASET OVERVIEW")
print(df.info())

print("\n")

print(df.describe())

# ----------------------------
# AQI Histogram
# ----------------------------

plt.figure(figsize=(8,5))
plt.hist(df["us_aqi"], bins=30)

plt.title("AQI Distribution")
plt.xlabel("US AQI")
plt.ylabel("Frequency")

plt.tight_layout()
plt.savefig("src/eda/plots/aqi_histogram.png")
plt.close()

# ----------------------------
# AQI Boxplot
# ----------------------------

plt.figure(figsize=(6,5))

plt.boxplot(df["us_aqi"])

plt.title("AQI Boxplot")

plt.tight_layout()
plt.savefig("src/eda/plots/aqi_boxplot.png")
plt.close()

# ----------------------------
# AQI Over Time
# ----------------------------

plt.figure(figsize=(14,5))

plt.plot(df["datetime"], df["us_aqi"])

plt.title("AQI Over Time")

plt.xlabel("Date")

plt.ylabel("US AQI")

plt.tight_layout()
plt.savefig("src/eda/plots/aqi_over_time.png")
plt.close()

print("\nEDA Part 1 Complete!")