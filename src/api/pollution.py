from src.api.client import APIClient
class PollutionClient(APIClient):

    def __init__(self):
        super().__init__(
            "https://api.openweathermap.org/data/2.5"
        )

    def history(self, lat, lon, start, end):

        return self.get(
            "air_pollution/history",
            {
                "lat": lat,
                "lon": lon,
                "start": start,
                "end": end,
            },
        )