import json
import shutil
from pathlib import Path

import joblib
import torch


def save_model(
    model,
    model_name,
    feature_columns,
    target_columns,
    input_size,
    output_size,
    scaler=None,
    metadata=None,
    validation_metrics=None,
    test_metrics=None,
):
    """
    Export a complete PyTorch model artifact.

    models/
        <model_name>/
            model.pt
            scaler.pkl (optional)
            metadata.json
            metrics.json
            feature_columns.json
            target_columns.json
    """

    project_root = Path(__file__).resolve().parents[3]

    models_root = project_root / "models"
    models_root.mkdir(exist_ok=True)

    model_dir = models_root / model_name

    # -----------------------------------------
    # Remove previous export
    # -----------------------------------------

    if model_dir.exists():
        shutil.rmtree(model_dir)

    model_dir.mkdir()

    # -----------------------------------------
    # Save model weights
    # -----------------------------------------

    torch.save(
        model.state_dict(),
        model_dir / "model.pt",
    )

    # -----------------------------------------
    # Save scaler
    # -----------------------------------------

    if scaler is not None:

        joblib.dump(
            scaler,
            model_dir / "scaler.pkl",
        )

    # -----------------------------------------
    # Save feature columns
    # -----------------------------------------

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

    # -----------------------------------------
    # Save target columns
    # -----------------------------------------

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

    # -----------------------------------------
    # Save metadata
    # -----------------------------------------

    metadata = dict(metadata or {})

    metadata.update(
        {
            "input_size": input_size,
            "output_size": output_size,
        }
    )

    with open(
        model_dir / "metadata.json",
        "w",
        encoding="utf-8",
    ) as f:

        json.dump(
            metadata,
            f,
            indent=4,
            sort_keys=True,
        )

 # -----------------------------------------
# Save evaluation metrics
# -----------------------------------------

    metrics = {
        "validation": validation_metrics,
        "test": test_metrics,
    }

    with open(
        model_dir / "metrics.json",
        "w",
        encoding="utf-8",
    ) as f:

        json.dump(
            metrics,
            f,
            indent=4,
            sort_keys=True,
        )

    print("=" * 50)
    print("Model Exported")
    print("=" * 50)
    print(f"Location : {model_dir}")

    return str(model_dir)

