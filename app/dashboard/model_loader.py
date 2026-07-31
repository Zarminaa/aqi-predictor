import json
import os

import joblib
import hopsworks
from dotenv import load_dotenv


def load_model_artifacts():

    load_dotenv()

    project = hopsworks.login(
        project="project_aqi",
        host="eu-west.cloud.hopsworks.ai",
        port=443,
        api_key_value=os.getenv("HOPSWORKS_API_KEY"),
    )

    mr = project.get_model_registry()

    model = mr.get_model(
        name="aqi_xgboost_3day_",
        version=1,
    )

    model_dir = model.download()

    print("Downloaded model files:")
    print(os.listdir(model_dir))

    xgb_model = joblib.load(
        os.path.join(model_dir, "model.pkl")
    )

    with open(
        os.path.join(model_dir, "metrics.json"),
        "r",
        encoding="utf-8",
    ) as f:
        metrics = json.load(f)

    return xgb_model, metrics, model_dir