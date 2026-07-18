import os
import matplotlib.pyplot as plt

os.makedirs("src/eda/plots", exist_ok=True)


def univariate_analysis(df):

    numeric_columns = df.select_dtypes(include="number").columns

    for column in numeric_columns:

        plt.figure(figsize=(8,5))

        plt.hist(df[column], bins=30)

        plt.title(f"{column} Distribution")

        plt.xlabel(column)

        plt.ylabel("Frequency")

        plt.tight_layout()

        plt.savefig(f"src/eda/plots/{column}_histogram.png")

        plt.close()

        plt.figure(figsize=(6,5))

        plt.boxplot(df[column])

        plt.title(f"{column} Boxplot")

        plt.tight_layout()

        plt.savefig(f"src/eda/plots/{column}_boxplot.png")

        plt.close()

    plt.figure(figsize=(15,5))

    plt.plot(df["datetime"], df["us_aqi"])

    plt.title("AQI Over Time")

    plt.tight_layout()

    plt.savefig("src/eda/plots/aqi_over_time.png")

    plt.close()