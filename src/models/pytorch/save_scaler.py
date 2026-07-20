from pathlib import Path
import joblib


def save_scaler(
    scaler,
    filename="pytorch_scaler.pkl",
):

    project_root = Path(__file__).resolve().parents[3]

    model_dir = project_root / "models"

    model_dir.mkdir(exist_ok=True)

    scaler_path = model_dir / filename

    joblib.dump(
        scaler,
        scaler_path,
    )

    print(f"Scaler saved to:\n{scaler_path}")