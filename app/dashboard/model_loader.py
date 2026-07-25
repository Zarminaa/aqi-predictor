import os
import joblib
import hopsworks
from dotenv import load_dotenv


def load_xgboost_model():

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
        version=1
    )

    model_dir = model.download()

    print("Downloaded model files:")
    print(os.listdir(model_dir))

    model_path = os.path.join(
        model_dir,
        "model.pkl"
    )

    xgb_model = joblib.load(model_path)

    return xgb_model