import json
import shutil
from pathlib import Path

import joblib


def save_model(
    model,
    model_name,
    feature_columns,
    target_columns,
    scaler=None,
    metadata=None,
):
    """
    Export a complete model artifact.

    The exported directory contains everything required
    for inference and model reproducibility.

    models/
        <model_name>/
            model.pkl
            scaler.pkl (optional)
            metadata.json
            feature_columns.json
            target_columns.json

    Parameters
    ----------
    model
        Trained model.

    model_name : str
        Name of the model.

    feature_columns : list[str]
        Ordered feature names.

    target_columns : list[str]
        Ordered target names.

    scaler : object, optional
        Preprocessing scaler used during training.

    metadata : dict, optional
        Additional model metadata.

    Returns
    -------
    pathlib.Path
        Exported model directory.
    """

    project_root = Path(__file__).resolve().parents[2]

    models_root = project_root / "models"
    models_root.mkdir(exist_ok=True)

    model_dir = models_root / model_name

    # --------------------------------------------------
    # Remove previous export
    # --------------------------------------------------

    if model_dir.exists():
        shutil.rmtree(model_dir)

    model_dir.mkdir()

    # --------------------------------------------------
    # Save trained model
    # --------------------------------------------------

    joblib.dump(
        model,
        model_dir / "model.pkl",
    )

    # --------------------------------------------------
    # Save scaler
    # --------------------------------------------------

    if scaler is not None:

        joblib.dump(
            scaler,
            model_dir / "scaler.pkl",
        )

    # --------------------------------------------------
    # Save feature columns
    # --------------------------------------------------

    with open(
        model_dir / "feature_columns.json",
        "w",
        encoding="utf-8",
    ) as f:

        json.dump(
            list(feature_columns),
            f,
            indent=4,
            sort_keys=True,
        )

    # --------------------------------------------------
    # Save target columns
    # --------------------------------------------------

    with open(
        model_dir / "target_columns.json",
        "w",
        encoding="utf-8",
    ) as f:

        json.dump(
            list(target_columns),
            f,
            indent=4,
            sort_keys=True,
        )

    # --------------------------------------------------
    # Save metadata
    # --------------------------------------------------

    with open(
        model_dir / "metadata.json",
        "w",
        encoding="utf-8",
    ) as f:

        json.dump(
            metadata or {},
            f,
            indent=4,
            sort_keys=True,
        )

    print("=" * 50)
    print("Model Exported")
    print("=" * 50)
    print(f"Location : {model_dir}")

    return str(model_dir)