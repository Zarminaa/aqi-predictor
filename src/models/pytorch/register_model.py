from src.hopsworks.model_registry import get_model_registry


def register_model(
    model_name,
    model_dir,
    validation_metrics,
    test_metrics,
    input_example,
    training_dataset_version=None,
):
    """
    Register a trained Scikit-learn model in the
    Hopsworks Model Registry.
    """

    mr = get_model_registry()

    metrics = {
        "validation_mae": validation_metrics["Overall"]["MAE"],
        "validation_rmse": validation_metrics["Overall"]["RMSE"],
        "validation_r2": validation_metrics["Overall"]["R2"],
        "test_mae": test_metrics["Overall"]["MAE"],
        "test_rmse": test_metrics["Overall"]["RMSE"],
        "test_r2": test_metrics["Overall"]["R2"],
    }

    model = mr.sklearn.create_model(
        name=model_name,
        description=(
            "Lahore AQI 3-Day Forecasting model "
            "trained using the Hopsworks Feature Store."
        ),
        metrics=metrics,
        input_example=input_example,
    )

    model.save(
        model_dir,
        keep_original_files=True,
    )

    print("=" * 50)
    print("Model Registered")
    print("=" * 50)
    print(f"Name    : {model.name}")
    print(f"Version : {model.version}")

    if training_dataset_version is not None:
        print(
            f"Training Dataset Version : "
            f"{training_dataset_version}"
        )

    return model