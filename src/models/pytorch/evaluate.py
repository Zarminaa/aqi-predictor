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
    Supports single-output and multi-output models.
    """

    predictions = predict(
        model=model,
        dataloader=dataloader,
        device=device,
    )


    # Convert pandas DataFrame/Series to numpy
    if hasattr(y_true, "values"):
        y_true = y_true.values

    if hasattr(predictions, "values"):
        predictions = predictions.values


    # Ensure numpy arrays
    y_true = np.asarray(y_true)
    predictions = np.asarray(predictions)


    # Ensure 2D shape
    if y_true.ndim == 1:
        y_true = y_true.reshape(-1, 1)

    if predictions.ndim == 1:
        predictions = predictions.reshape(-1, 1)


    results = {}

    print("=" * 50)
    print("PyTorch Model Evaluation")
    print("=" * 50)


    # Check shapes
    print(f"Actual shape      : {y_true.shape}")
    print(f"Prediction shape  : {predictions.shape}")


    # Per-output metrics
    for i in range(y_true.shape[1]):

        mae = mean_absolute_error(
            y_true[:, i],
            predictions[:, i],
        )

        rmse = np.sqrt(
            mean_squared_error(
                y_true[:, i],
                predictions[:, i],
            )
        )

        r2 = r2_score(
            y_true[:, i],
            predictions[:, i],
        )


        print(f"\nDay {i+1}")
        print("-" * 20)
        print(f"MAE  : {mae:.3f}")
        print(f"RMSE : {rmse:.3f}")
        print(f"R²   : {r2:.3f}")


        results[f"Day_{i+1}"] = {
            "MAE": mae,
            "RMSE": rmse,
            "R2": r2,
        }


    # Overall metrics
    overall_mae = mean_absolute_error(
        y_true,
        predictions,
    )

    overall_rmse = np.sqrt(
        mean_squared_error(
            y_true,
            predictions,
        )
    )

    overall_r2 = r2_score(
        y_true,
        predictions,
        multioutput="uniform_average",
    )


    print("\nOverall")
    print("=" * 50)

    print(f"MAE  : {overall_mae:.3f}")
    print(f"RMSE : {overall_rmse:.3f}")
    print(f"R²   : {overall_r2:.3f}")


    results["Overall"] = {
        "MAE": overall_mae,
        "RMSE": overall_rmse,
        "R2": overall_r2,
    }


    return results