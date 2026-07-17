from src.api.client import APIClient


class WeatherClient(APIClient):

    def current(self, lat, lon):
        """
        Fetch the current weather for a location.
        """
        return self.get(
            "weather",
            params={
                "lat": lat,
                "lon": lon,
                "units": "metric",
            },
        )