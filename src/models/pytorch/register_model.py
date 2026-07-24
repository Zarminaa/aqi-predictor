from src.hopsworks.model_registry import get_model_registry


def register_model(
    model_name,
    model_path,
    validation_metrics,
    test_metrics,
    training_dataset_version=None,
):

    mr = get_model_registry()

    metrics = {
        "validation_mae": validation_metrics["Overall"]["MAE"],
        "validation_rmse": validation_metrics["Overall"]["RMSE"],
        "validation_r2": validation_metrics["Overall"]["R2"],
        "test_mae": test_metrics["Overall"]["MAE"],
        "test_rmse": test_metrics["Overall"]["RMSE"],
        "test_r2": test_metrics["Overall"]["R2"],
    }

    model = mr.torch.create_model(
        name=model_name,
        metrics=metrics,
        description=(
            "Lahore AQI 3-Day Forecasting PyTorch Model "
            "using Hopsworks Feature Store"
        ),
    )

    model.save(
        model_path,
        keep_original_files=True,
    )

    print("=" * 50)
    print("Model Registered")
    print("=" * 50)
    print(f"Name    : {model_name}")
    print(f"Version : {model.version}")

    if training_dataset_version is not None:
        print(
            f"Training Dataset Version : "
            f"{training_dataset_version}"
        )

    return model