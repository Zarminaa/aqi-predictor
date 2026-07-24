from datetime import datetime, timezone


def create_model_metadata(
    model_name,
    framework,
    algorithm,
    training_dataset_version,
    feature_columns,
    target_columns,
    requires_scaling,
    feature_view_name="aqi_training_view",
    feature_view_version=1,
):
    """
    Create metadata describing a trained model.

    Parameters
    ----------
    model_name : str
        Registered model name.

    framework : str
        ML framework (e.g. scikit-learn, PyTorch).

    algorithm : str
        Algorithm name (e.g. Ridge, Random Forest).

    training_dataset_version : int | None
        Hopsworks training dataset version.

    feature_columns : list[str]
        Ordered feature names.

    target_columns : list[str]
        Ordered target names.

    requires_scaling : bool
        Whether inference requires a scaler.

    feature_view_name : str
        Feature View used for training.

    feature_view_version : int
        Feature View version.

    Returns
    -------
    dict
        Model metadata.
    """

    return {
        "model_name": model_name,
        "framework": framework,
        "algorithm": algorithm,
        "feature_view": feature_view_name,
        "feature_view_version": feature_view_version,
        "training_dataset_version": training_dataset_version,
        "feature_count": len(feature_columns),
        "target_count": len(target_columns),
        "feature_columns": list(feature_columns),
        "target_columns": list(target_columns),
        "requires_scaling": requires_scaling,
        "created_at": datetime.now(
            timezone.utc
        ).isoformat(),
    }