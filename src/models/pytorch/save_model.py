from pathlib import Path

import torch


def save_model(
    model,
    filename="ann.pt",
):
    """
    Save a trained PyTorch model.
    """

    project_root = Path(__file__).resolve().parents[3]

    model_dir = project_root / "models"

    model_dir.mkdir(exist_ok=True)

    model_path = model_dir / filename

    torch.save(
        model.state_dict(),
        model_path,
    )

    print(f"Model saved to:\n{model_path}")