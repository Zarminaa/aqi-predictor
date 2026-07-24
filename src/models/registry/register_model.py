import os
import hopsworks

from dotenv import load_dotenv


def register_model(
    model_name,
    model_path,
    validation_metrics,
    test_metrics,
):
    """
    Register a trained model in the Hopsworks Model Registry.
    """

    load_dotenv()

    project = hopsworks.login(
        project="project_aqi",
        host="eu-west.cloud.hopsworks.ai",
        port=443,
        api_key_value=os.getenv("HOPSWORKS_API_KEY"),
    )

    mr = project.get_model_registry()

    metrics = {
        "validation_mae": validation_metrics["Overall"]["MAE"],
        "validation_rmse": validation_metrics["Overall"]["RMSE"],
        "validation_r2": validation_metrics["Overall"]["R2"],
        "test_mae": test_metrics["Overall"]["MAE"],
        "test_rmse": test_metrics["Overall"]["RMSE"],
        "test_r2": test_metrics["Overall"]["R2"],
    }

    sklearn_model = mr.sklearn.create_model(
        name=model_name,
        metrics=metrics,
        description="3-Day AQI Forecasting Model",
    )

    sklearn_model.save(model_path)

    print(f"Registered {model_name}")
    print(f"Version: {sklearn_model.version}")