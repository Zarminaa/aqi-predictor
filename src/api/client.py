import os
import requests
from dotenv import load_dotenv

# Load variables from .env
load_dotenv()

API_KEY = os.getenv("OPENWEATHER_API_KEY")


class APIClient:

    def __init__(self, base_url):
        if API_KEY is None:
            raise ValueError(
                "OPENWEATHER_API_KEY not found in .env"
            )
        self.base_url = base_url
        self.api_key = API_KEY

    def get(self, endpoint="", params=None):

        if params is None:
            params = {}

        params["appid"] = self.api_key

        url = f"{self.base_url}/{endpoint}"

        response = requests.get(
            url,
            params=params,
            timeout=30,
        )

        response.raise_for_status()

        return response.json()