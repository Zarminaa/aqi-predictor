from dateutil.relativedelta import relativedelta
import pandas as pd


from src.api.pollution import PollutionClient
from src.configs.config import (
    LAT,
    LON,
    START_DATE,
    END_DATE,
    POLLUTION_OUTPUT_FILE,
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
    Fetch historical pollution data for a single time window.
    """
    return client.history(
        lat=LAT,
        lon=LON,
        start=int(start.timestamp()),
        end=int(end.timestamp()),
    )


def parse_response(data):
    """
    Convert OpenWeather API response into a list of dictionaries.
    """
    records = []

    for record in data["list"]:
        records.append(
            {
                "datetime": pd.to_datetime(
                    record["dt"],
                    unit="s",
                    utc=True,
                ),
                "aqi": record["main"]["aqi"],
                "co": record["components"]["co"],
                "no": record["components"]["no"],
                "no2": record["components"]["no2"],
                "o3": record["components"]["o3"],
                "so2": record["components"]["so2"],
                "pm2_5": record["components"]["pm2_5"],
                "pm10": record["components"]["pm10"],
                "nh3": record["components"]["nh3"],
            }
        )

    return records


def save_csv(records):
    """
    Save all pollution records to CSV.
    """
    df = pd.DataFrame(records)

    # Sort chronologically
    df.sort_values("datetime", inplace=True)

    # Remove duplicate timestamps caused by overlapping windows
    df.drop_duplicates(
        subset="datetime",
        keep="first",
        inplace=True,
    )

    # Clean index
    df.reset_index(drop=True, inplace=True)

    # Save
    df.to_csv(
        POLLUTION_OUTPUT_FILE,
        index=False,
    )

    print(f"Saved {len(df)} unique records to '{POLLUTION_OUTPUT_FILE}'.")


def run_pollution_pipeline():
    """
    Run the complete pollution data collection pipeline.
    """
    print("=" * 60)
    print("Starting Pollution Pipeline")
    print("=" * 60)

    client = PollutionClient()

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
    print("Pollution Pipeline Finished")
    print("=" * 60)
    print(f"Total Records Collected : {len(all_records)}")
    print(f"Failed Windows          : {len(failed_windows)}")
    print(f"Output File             : {POLLUTION_OUTPUT_FILE}")

    if failed_windows:
        print("\nFailed Windows:")
        for start, end in failed_windows:
            print(f"  - {start.date()} -> {end.date()}")

    print("=" * 60)


if __name__ == "__main__":
    run_pollution_pipeline()