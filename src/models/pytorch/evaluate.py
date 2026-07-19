from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score,
)

import numpy as np

from .predict import predict


def evaluate_model(
    model,
    dataloader,
    y_true,
    device,
):
    """
    Evaluate a trained PyTorch model.
    """

    predictions = predict(
        model=model,
        dataloader=dataloader,
        device=device,
    )

    mae = mean_absolute_error(
        y_true,
        predictions,
    )

    rmse = np.sqrt(
        mean_squared_error(
            y_true,
            predictions,
        )
    )

    r2 = r2_score(
        y_true,
        predictions,
    )

    print("=" * 50)
    print("PyTorch Model Evaluation")
    print("=" * 50)
    print(f"MAE  : {mae:.3f}")
    print(f"RMSE : {rmse:.3f}")
    print(f"R²   : {r2:.3f}")

    return {
        "MAE": mae,
        "RMSE": rmse,
        "R2": r2,
    }