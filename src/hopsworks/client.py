import os

import hopsworks
from dotenv import load_dotenv


def get_project():

    load_dotenv()

    project = hopsworks.login(
        project="project_aqi",
        host="eu-west.cloud.hopsworks.ai",
        port=443,
        api_key_value=os.getenv("HOPSWORKS_API_KEY"),
    )

    return project