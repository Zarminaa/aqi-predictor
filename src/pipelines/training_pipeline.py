from src.data.load_data import load_features
from src.data.split_data import split_data

from src.preprocessing.feature_scaling import scale_features

from src.models.evaluate import evaluate_model
from src.models.save_model import save_model
from src.models.save_predictions import save_predictions
from src.models.pytorch.save_scaler import save_scaler

from src.models.random_forest.train import train_random_forest
from src.models.ridge.train import train_ridge
from src.models.xgboost.train import train_xgboost


def train_pipeline(
    trainer,
    model_name,
    target,
):
    """
    Generic training pipeline that can train any model.

    Parameters
    ----------
    trainer : callable
        Function that trains and returns a model.

    model_name : str
        Name of the model.

    target : str or list[str]
        Target column(s).
    """

    print("=" * 60)
    print(f"{model_name.upper()} TRAINING PIPELINE")
    print("=" * 60)

    # ----------------------------------------------------
    # Load Dataset
    # ----------------------------------------------------
    print("\nLoading dataset...")

    df = load_features()

    print(f"Dataset Shape: {df.shape}")

    # ----------------------------------------------------
    # Split Dataset
    # ----------------------------------------------------
    print("\nSplitting dataset...")

    (
        X_train,
        X_val,
        X_test,
        y_train,
        y_val,
        y_test,
    ) = split_data(
        df=df,
        target=target,
    )

    print(f"Training Samples   : {len(X_train)}")
    print(f"Validation Samples : {len(X_val)}")
    print(f"Testing Samples    : {len(X_test)}")

    print(f"X_train shape: {X_train.shape}")
    print(f"y_train shape: {y_train.shape}")

    print("\nFirst target row:")
    print(y_train.iloc[0])

    # ----------------------------------------------------
    # Feature Scaling (Only if required)
    # ----------------------------------------------------
    if getattr(trainer, "requires_scaling", False):

        print("\nScaling features...")

        X_train, X_val, X_test, scaler = scale_features(
            X_train,
            X_val,
            X_test,
        )

        save_scaler(
            scaler=scaler,
            filename=f"{model_name}_scaler.pkl",
        )

    # ----------------------------------------------------
    # Train Model
    # ----------------------------------------------------
    print(f"\nTraining {model_name}...")

    model = trainer(
        X_train=X_train,
        y_train=y_train,
    )

    print("Training completed!")

    # ----------------------------------------------------
    # Validation Evaluation
    # ----------------------------------------------------
    print("\nValidation Results")

    validation_metrics = evaluate_model(
        model=model,
        X=X_val,
        y=y_val,
    )

    # ----------------------------------------------------
    # Test Evaluation
    # ----------------------------------------------------
    print("\nTest Results")

    test_metrics = evaluate_model(
        model=model,
        X=X_test,
        y=y_test,
    )

    # ----------------------------------------------------
    # Save Predictions
    # ----------------------------------------------------
    print("\nSaving predictions...")

    predictions = model.predict(X_test)

    if isinstance(target, list):
        prediction_filename = f"{model_name}_multi_output_predictions.csv"
    else:
        prediction_filename = f"{model_name}_{target}_predictions.csv"

    save_predictions(
        y_true=y_test,
        y_pred=predictions,
        filename=prediction_filename,
    )

    # ----------------------------------------------------
    # Save Model
    # ----------------------------------------------------
    print("\nSaving model...")

    if isinstance(target, list):
        model_filename = f"{model_name}_multi_output.pkl"
    else:
        model_filename = f"{model_name}_{target}.pkl"

    save_model(
        model=model,
        filename=model_filename,
    )

    print("\nTraining pipeline completed successfully!")

    return {
        "model": model,
        "validation_metrics": validation_metrics,
        "test_metrics": test_metrics,
    }


def main():

    TARGET_COLUMNS = [
        "target_day1",
        "target_day2",
        "target_day3",
    ]

    # train_pipeline(
    #     trainer=train_ridge,
    #     model_name="ridge",
    #     target=TARGET_COLUMNS,
    # )

    # train_pipeline(
    #     trainer=train_random_forest,
    #     model_name="random_forest",
    #     target=TARGET_COLUMNS,
    # )

    train_pipeline(
        trainer=train_xgboost,
        model_name="xgboost",
        target=TARGET_COLUMNS,
    )


if __name__ == "__main__":
    main()