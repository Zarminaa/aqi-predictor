import os
import requests
from dotenv import load_dotenv

# Load variables from .env
load_dotenv()

API_KEY = os.getenv("OPENWEATHER_API_KEY")

BASE_URL = "https://api.openweathermap.org/data/2.5"


class APIClient:
    """Reusable client for making requests to OpenWeather."""

    def __init__(self):
        if API_KEY is None:
            raise ValueError(
                "OPENWEATHER_API_KEY not found in .env"
            )

        self.api_key = API_KEY

    def get(self, endpoint, params=None):
        """
        Send a GET request to the OpenWeather API.
        """

        if params is None:
            params = {}

        params["appid"] = self.api_key

        url = f"{BASE_URL}/{endpoint}"

        response = requests.get(
            url,
            params=params,
            timeout=30,
        )

        response.raise_for_status()

        return response.json()
    

