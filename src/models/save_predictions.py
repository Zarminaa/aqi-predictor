from pathlib import Path
import pandas as pd


def save_predictions(
    y_true,
    y_pred,
    filename="predictions.csv",
):
    """
    Save actual vs predicted values.
    """

    results = pd.DataFrame()

    if y_true.ndim == 1:
        results["Actual"] = y_true
        results["Predicted"] = y_pred

    else:
        for i in range(y_true.shape[1]):
            results[f"Actual_Day{i+1}"] = y_true.iloc[:, i]
            results[f"Predicted_Day{i+1}"] = y_pred[:, i]

    project_root = Path(__file__).resolve().parents[2]

    output_dir = project_root / "predictions"
    output_dir.mkdir(exist_ok=True)

    output_path = output_dir / filename

    results.to_csv(
        output_path,
        index=False,
    )

    print(f"Predictions saved to:\n{output_path}")