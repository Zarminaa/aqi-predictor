import os
import hopsworks
from dotenv import load_dotenv


def get_feature_group():

    load_dotenv()

    project = hopsworks.login(
        project="project_aqi",
        host="eu-west.cloud.hopsworks.ai",
        port=443,
        api_key_value=os.getenv("HOPSWORKS_API_KEY")
    )

    fs = project.get_feature_store()

    fg = fs.get_feature_group(
        name="aqi_features",
        version=1
    )

    return fg