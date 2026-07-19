from pathlib import Path
import joblib


def save_model(
    model,
    filename="random_forest_day1.pkl",
):
    """
    Save trained model.
    """

    project_root = Path(__file__).resolve().parents[2]

    model_dir = project_root / "models"

    model_dir.mkdir(exist_ok=True)

    model_path = model_dir / filename

    joblib.dump(model, model_path)

    print(f"Model saved to:\n{model_path}")