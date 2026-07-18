import matplotlib.pyplot as plt


def time_analysis(df):

    df = df.copy()

    df["hour"] = df["datetime"].dt.hour
    df["month"] = df["datetime"].dt.month
    df["weekday"] = df["datetime"].dt.day_name()

    hourly = df.groupby("hour")["us_aqi"].mean()

    plt.figure(figsize=(10,5))

    plt.plot(hourly.index, hourly.values, marker="o")

    plt.title("Average AQI by Hour")

    plt.xlabel("Hour")

    plt.ylabel("Average AQI")

    plt.grid(True)

    plt.tight_layout()

    plt.savefig("src/eda/plots/hourly_aqi.png")

    plt.close()

    monthly = df.groupby("month")["us_aqi"].mean()

    plt.figure(figsize=(10,5))

    plt.plot(monthly.index, monthly.values, marker="o")

    plt.title("Average AQI by Month")

    plt.xlabel("Month")

    plt.ylabel("Average AQI")

    plt.grid(True)

    plt.tight_layout()

    plt.savefig("src/eda/plots/monthly_aqi.png")

    plt.close()

    order = [

        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday",

    ]

    weekday = df.groupby("weekday")["us_aqi"].mean().reindex(order)

    plt.figure(figsize=(10,5))

    plt.plot(weekday.index, weekday.values, marker="o")

    plt.title("Average AQI by Day of Week")

    plt.ylabel("Average AQI")

    plt.xticks(rotation=45)

    plt.tight_layout()

    plt.savefig("src/eda/plots/weekday_aqi.png")

    plt.close()