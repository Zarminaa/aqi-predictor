from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score,
)
import numpy as np


def evaluate_model(model, X, y):
    """
    Evaluate a trained model.
    """

    predictions = model.predict(X)

    mae = mean_absolute_error(y, predictions)

    rmse = np.sqrt(
        mean_squared_error(y, predictions)
    )

    r2 = r2_score(y, predictions)

    print("=" * 50)
    print("Model Evaluation")
    print("=" * 50)
    print(f"MAE  : {mae:.3f}")
    print(f"RMSE : {rmse:.3f}")
    print(f"R²   : {r2:.3f}")

    return {
        "MAE": mae,
        "RMSE": rmse,
        "R2": r2,
    }