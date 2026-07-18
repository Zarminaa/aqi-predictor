import os

import pandas as pd
import matplotlib.pyplot as plt


class EDAAnalyzer:

    def __init__(self, dataframe, output_dir="src/eda/plots"):

        self.df = dataframe.copy()
        self.output_dir = output_dir

        os.makedirs(self.output_dir, exist_ok=True)

    # ---------------------------------------------------
    # Helper
    # ---------------------------------------------------

    def save_plot(self, filename):

        plt.tight_layout()
        plt.savefig(os.path.join(self.output_dir, filename))
        plt.close()

    # ---------------------------------------------------
    # Dataset Overview
    # ---------------------------------------------------

    def dataset_overview(self):

        print("=" * 60)
        print("DATASET OVERVIEW")
        print("=" * 60)

        print(self.df.info())

        print("\n")

        print(self.df.describe())

    # ---------------------------------------------------
    # Histograms
    # ---------------------------------------------------

    def histograms(self):

        numeric_columns = self.df.select_dtypes(include="number").columns

        for column in numeric_columns:

            plt.figure(figsize=(8,5))

            plt.hist(self.df[column], bins=30)

            plt.title(f"{column} Distribution")

            plt.xlabel(column)

            plt.ylabel("Frequency")

            self.save_plot(f"{column}_histogram.png")

    # ---------------------------------------------------
    # Boxplots
    # ---------------------------------------------------

    def boxplots(self):

        numeric_columns = self.df.select_dtypes(include="number").columns

        for column in numeric_columns:

            plt.figure(figsize=(6,5))

            plt.boxplot(self.df[column])

            plt.title(f"{column} Boxplot")

            self.save_plot(f"{column}_boxplot.png")

    # ---------------------------------------------------
    # AQI Time Series
    # ---------------------------------------------------

    def aqi_over_time(self):

        plt.figure(figsize=(15,5))

        plt.plot(
            self.df["datetime"],
            self.df["us_aqi"]
        )

        plt.title("AQI Over Time")

        plt.xlabel("Datetime")

        plt.ylabel("US AQI")

        self.save_plot("aqi_over_time.png")

    # ---------------------------------------------------
    # Correlation
    # ---------------------------------------------------

    def correlation_analysis(self):

        corr = self.df.select_dtypes(include="number").corr()

        fig, ax = plt.subplots(figsize=(12,10))

        image = ax.imshow(corr)

        ax.set_xticks(range(len(corr.columns)))
        ax.set_xticklabels(corr.columns, rotation=90)

        ax.set_yticks(range(len(corr.columns)))
        ax.set_yticklabels(corr.columns)

        fig.colorbar(image)

        self.save_plot("correlation_heatmap.png")

        print("\nCorrelation with AQI\n")

        print(
            corr["us_aqi"]
            .sort_values(ascending=False)
        )

    # ---------------------------------------------------
    # Scatter Plots
    # ---------------------------------------------------

    def scatter_plots(self):

        features = [

            "pm2_5",
            "pm10",
            "carbon_monoxide",
            "nitrogen_dioxide",
            "ozone",
            "temperature_2m",
            "relative_humidity_2m",
            "wind_speed_10m",

        ]

        for feature in features:

            plt.figure(figsize=(6,5))

            plt.scatter(
                self.df[feature],
                self.df["us_aqi"],
                alpha=0.25
            )

            plt.xlabel(feature)

            plt.ylabel("US AQI")

            plt.title(f"{feature} vs AQI")

            self.save_plot(f"{feature}_vs_aqi.png")

    # ---------------------------------------------------
    # Time Analysis
    # ---------------------------------------------------

    def time_analysis(self):

        self.df["hour"] = self.df["datetime"].dt.hour
        self.df["month"] = self.df["datetime"].dt.month
        self.df["weekday"] = self.df["datetime"].dt.day_name()

        # Hourly

        hourly = (
            self.df
            .groupby("hour")["us_aqi"]
            .mean()
        )

        plt.figure(figsize=(10,5))

        plt.plot(hourly.index, hourly.values, marker="o")

        plt.title("Average AQI by Hour")

        plt.xlabel("Hour")

        plt.ylabel("Average AQI")

        plt.grid(True)

        self.save_plot("hourly_aqi.png")

        # Monthly

        monthly = (
            self.df
            .groupby("month")["us_aqi"]
            .mean()
        )

        plt.figure(figsize=(10,5))

        plt.plot(monthly.index, monthly.values, marker="o")

        plt.title("Average AQI by Month")

        plt.xlabel("Month")

        plt.ylabel("Average AQI")

        plt.grid(True)

        self.save_plot("monthly_aqi.png")

        # Weekday

        order = [

            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday",
            "Saturday",
            "Sunday",

        ]

        weekday = (
            self.df
            .groupby("weekday")["us_aqi"]
            .mean()
            .reindex(order)
        )

        plt.figure(figsize=(10,5))

        plt.plot(
            weekday.index,
            weekday.values,
            marker="o"
        )

        plt.title("Average AQI by Weekday")

        plt.ylabel("Average AQI")

        plt.xticks(rotation=45)

        self.save_plot("weekday_aqi.png")

    # ---------------------------------------------------
    # Run Everything
    # ---------------------------------------------------

    def run(self):

        self.dataset_overview()

        self.histograms()

        self.boxplots()

        self.aqi_over_time()

        self.correlation_analysis()

        self.scatter_plots()

        self.time_analysis()

        print("\nEDA Complete!")