from dateutil.relativedelta import relativedelta
import pandas as pd

from src.api.weather import WeatherClient
from src.config import (
    LAT,
    LON,
    START_DATE,
    END_DATE,
    OUTPUT_FILE,
)


def generate_windows(months=6):
    """
    Generate consecutive time windows between START_DATE and END_DATE.
    """
    windows = []

    current_start = START_DATE

    while current_start < END_DATE:
        current_end = current_start + relativedelta(months=months)

        if current_end > END_DATE:
            current_end = END_DATE

        windows.append((current_start, current_end))

        current_start = current_end

    return windows


def fetch_window(client, start, end):
    """
    Fetch historical weather data for a single time window.
    """
    return client.history(
        lat=LAT,
        lon=LON,
        start=int(start.timestamp()),
        end=int(end.timestamp()),
    )


def parse_response(data):
    """
    Convert OpenWeather weather response into a list of dictionaries.
    """
    records = []

    for record in data["list"]:

        weather = record["weather"][0]

        records.append(
            {
                "datetime": pd.to_datetime(
                    record["dt"],
                    unit="s",
                    utc=True,
                ),

                "temperature": record["main"]["temp"],
                "temp_min": record["main"]["temp_min"],
                "temp_max": record["main"]["temp_max"],

                "pressure": record["main"]["pressure"],
                "humidity": record["main"]["humidity"],

                "sea_level": record["main"].get("sea_level"),
                "grnd_level": record["main"].get("grnd_level"),

                "wind_speed": record["wind"]["speed"],
                "wind_deg": record["wind"]["deg"],

                "clouds": record["clouds"]["all"],

                "weather_main": weather["main"],
                "weather_description": weather["description"],
            }
        )

    return records


def save_csv(records):
    """
    Save all weather records to CSV.
    """
    df = pd.DataFrame(records)

    df.sort_values("datetime", inplace=True)

    df.drop_duplicates(
        subset="datetime",
        keep="first",
        inplace=True,
    )

    df.reset_index(drop=True, inplace=True)

    df.to_csv(
        OUTPUT_FILE,
        index=False,
    )

    print(f"Saved {len(df)} unique records to '{OUTPUT_FILE}'.")


def run_weather_pipeline():
    """
    Run the complete weather data collection pipeline.
    """
    print("=" * 60)
    print("Starting Weather Pipeline")
    print("=" * 60)

    client = WeatherClient()

    windows = generate_windows()

    print(f"Generated {len(windows)} time windows.\n")

    all_records = []
    failed_windows = []

    for i, (start, end) in enumerate(windows, start=1):

        print(
            f"[{i}/{len(windows)}] "
            f"Fetching {start.date()} → {end.date()}"
        )

        try:
            response = fetch_window(
                client,
                start,
                end,
            )

            if "list" not in response or not response["list"]:
                print("    No data returned.\n")
                continue

            rows = parse_response(response)

            all_records.extend(rows)

            print(f"    Retrieved {len(rows)} hourly records.\n")

        except Exception as e:
            print(f"    ERROR: {e}\n")
            failed_windows.append((start, end))
            continue

    if all_records:
        save_csv(all_records)
    else:
        print("No records were collected. CSV was not created.")
        return

    print("=" * 60)
    print("Weather Pipeline Finished")
    print("=" * 60)
    print(f"Total Records Collected : {len(all_records)}")
    print(f"Failed Windows          : {len(failed_windows)}")
    print(f"Output File             : {OUTPUT_FILE}")

    if failed_windows:
        print("\nFailed Windows:")
        for start, end in failed_windows:
            print(f"  - {start.date()} -> {end.date()}")

    print("=" * 60)


if __name__ == "__main__":
    run_weather_pipeline()