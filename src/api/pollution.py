from datetime import datetime, timezone
import json
from pathlib import Path

from src.api.client import APIClient


class PollutionClient(APIClient):

    def history(self, lat, lon, start, end):
        return self.get(
            "air_pollution/history",
            params={
                "lat": lat,
                "lon": lon,
                "start": start,
                "end": end,
            },
        )


def to_unix(year, month, day):
    return int(
        datetime(
            year,
            month,
            day,
            tzinfo=timezone.utc,
        ).timestamp()
    )

