from datetime import datetime, timezone

LAT = 31.5204
LON = 74.3587

START_DATE = datetime(
    2020,
    7,
    1,
    tzinfo=timezone.utc,
)

END_DATE = datetime(
    2026,
    7,
    2,
    tzinfo=timezone.utc,
)

POLLUTION_OUTPUT_FILE = "data/raw/pollution.csv"
