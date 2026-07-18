import matplotlib.pyplot as plt


def correlation_analysis(df):

    corr = df.select_dtypes(include="number").corr()

    fig, ax = plt.subplots(figsize=(12,10))

    image = ax.imshow(corr)

    ax.set_xticks(range(len(corr.columns)))
    ax.set_xticklabels(corr.columns, rotation=90)

    ax.set_yticks(range(len(corr.columns)))
    ax.set_yticklabels(corr.columns)

    fig.colorbar(image)

    plt.tight_layout()

    plt.savefig("src/eda/plots/correlation_heatmap.png")

    plt.close()

    print("\nCorrelation with AQI\n")

    print(corr["us_aqi"].sort_values(ascending=False))

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

        plt.scatter(df[feature], df["us_aqi"], alpha=0.3)

        plt.xlabel(feature)

        plt.ylabel("US AQI")

        plt.title(f"{feature} vs AQI")

        plt.tight_layout()

        plt.savefig(f"src/eda/plots/{feature}_vs_aqi.png")

        plt.close()