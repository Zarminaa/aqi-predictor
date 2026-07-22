from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score,
)
import numpy as np


def evaluate_model(model, X, y):
    """
    Evaluate a trained model.

    Supports both single-output and multi-output regression.
    """

    predictions = model.predict(X)

    print("=" * 50)
    print("Model Evaluation")
    print("=" * 50)

    # ----------------------------------------------------
    # Single-output regression
    # ----------------------------------------------------
    if predictions.ndim == 1:

        mae = mean_absolute_error(y, predictions)

        rmse = np.sqrt(
            mean_squared_error(y, predictions)
        )

        r2 = r2_score(y, predictions)

        print(f"MAE  : {mae:.3f}")
        print(f"RMSE : {rmse:.3f}")
        print(f"R²   : {r2:.3f}")

        return {
            "MAE": mae,
            "RMSE": rmse,
            "R2": r2,
        }

    # ----------------------------------------------------
    # Multi-output regression
    # ----------------------------------------------------
    metrics = {}

    for i in range(predictions.shape[1]):

        mae = mean_absolute_error(
            y.iloc[:, i],
            predictions[:, i],
        )

        rmse = np.sqrt(
            mean_squared_error(
                y.iloc[:, i],
                predictions[:, i],
            )
        )

        r2 = r2_score(
            y.iloc[:, i],
            predictions[:, i],
        )

        print(f"\nDay {i + 1}")
        print("-" * 20)
        print(f"MAE  : {mae:.3f}")
        print(f"RMSE : {rmse:.3f}")
        print(f"R²   : {r2:.3f}")

        metrics[f"Day{i+1}"] = {
            "MAE": mae,
            "RMSE": rmse,
            "R2": r2,
        }

    overall_mae = mean_absolute_error(
        y,
        predictions,
    )

    overall_rmse = np.sqrt(
        mean_squared_error(
            y,
            predictions,
        )
    )

    overall_r2 = r2_score(
        y,
        predictions,
    )

    print("\n" + "=" * 50)
    print("Overall")
    print("=" * 50)
    print(f"MAE  : {overall_mae:.3f}")
    print(f"RMSE : {overall_rmse:.3f}")
    print(f"R²   : {overall_r2:.3f}")

    metrics["Overall"] = {
        "MAE": overall_mae,
        "RMSE": overall_rmse,
        "R2": overall_r2,
    }

    return metrics