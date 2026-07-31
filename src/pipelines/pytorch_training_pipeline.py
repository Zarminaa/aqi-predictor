# Force PyTorch to initialize first
from src.models.pytorch.dataset import create_dataloader
from src.models.pytorch.train import train_pytorch
from src.models.pytorch.evaluate import evaluate_model
from src.models.pytorch.save_model import save_model
from src.models.pytorch.register_model import register_model

from src.data.split_data import split_data
from src.models.registry.metadata import create_model_metadata
from src.preprocessing.feature_scaling import scale_features

from src.hopsworks.training_dataset import (
    load_training_data,
    get_training_dataset,
)

MODEL_NAME = "aqi_pytorch_3day"

def train_pipeline(
    target,
    training_dataset_version=None,
):
    """
    PyTorch training pipeline.

    Parameters
    ----------
    target : str | list[str]
        Target column(s).

    training_dataset_version : int | None
        Hopsworks materialized training dataset version.
        If None, loads directly from the Feature View.
    """

    print("=" * 60)
    print("PYTORCH TRAINING PIPELINE")
    print("=" * 60)


    
    # ----------------------------------------------------
    # Load Dataset
    # ----------------------------------------------------

    print("\nLoading dataset...")

    if training_dataset_version is None:

        print(
            "Loading latest data from Feature View..."
        )

        df = load_training_data()

    else:

        print(
            f"Loading Training Dataset Version "
            f"{training_dataset_version}..."
        )

        df = get_training_dataset(
            version=training_dataset_version,
        )

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

    print(f"\nX_train shape: {X_train.shape}")
    print(f"y_train shape: {y_train.shape}")
    print("\nFirst target row:")
    print(y_train.iloc[0])

    # ----------------------------------------------------
    # Feature Scaling
    # ----------------------------------------------------

    print("\nScaling features...")

    X_train, X_val, X_test, scaler = scale_features(
    X_train,
    X_val,
    X_test,
)
    

    # ----------------------------------------------------
    # Create DataLoaders
    # ----------------------------------------------------

    print("\nCreating DataLoaders...")

    train_loader = create_dataloader(
        X_train,
        y_train,
        shuffle=True,
    )

    val_loader = create_dataloader(
        X_val,
        y_val,
    )

    test_loader = create_dataloader(
        X_test,
        y_test,
    )

    # ----------------------------------------------------
    # Output Size
    # ----------------------------------------------------

    if y_train.ndim == 1:
        output_size = 1
    else:
        output_size = y_train.shape[1]

    # ----------------------------------------------------
    # Train Model
    # ----------------------------------------------------

    print("\nTraining PyTorch Model...")

    model, device = train_pytorch(
        train_loader=train_loader,
        val_loader=val_loader,
        y_val=y_val,
        input_size=X_train.shape[1],
        output_size=output_size,
    )
    
    print("\nTraining completed!")

    # ----------------------------------------------------
    # Validation Evaluation
    # ----------------------------------------------------

    print("\nValidation Results")

    validation_metrics = evaluate_model(
        model=model,
        dataloader=val_loader,
        y_true=y_val,
        device=device,
    )

    # ----------------------------------------------------
    # Test Evaluation
    # ----------------------------------------------------

    print("\nTest Results")

    test_metrics = evaluate_model(
        model=model,
        dataloader=test_loader,
        y_true=y_test,
        device=device,
    )

    metadata = create_model_metadata(
        model_name=MODEL_NAME,
        framework="PyTorch",
        algorithm=model.__class__.__name__,
        training_dataset_version=training_dataset_version,
        feature_columns=X_train.columns.tolist(),
        target_columns=(
            target
            if isinstance(target, list)
            else [target]
        ),
        requires_scaling=scaler is not None,
    )

    # ----------------------------------------------------
    # Save Model
    # ----------------------------------------------------

    print("\nSaving model...")

    model_dir = save_model(
    model=model,
    model_name=MODEL_NAME,
    feature_columns=X_train.columns.tolist(),
    target_columns=(
        target
        if isinstance(target, list)
        else [target]
    ),
    input_size=X_train.shape[1],
    output_size=output_size,
    scaler=scaler,
    metadata=metadata,
    validation_metrics=validation_metrics,
    test_metrics=test_metrics,
)

    # ----------------------------------------------------
    # Register Model
    # ----------------------------------------------------

    print("\nRegistering model...")

    register_model(
    model_name=MODEL_NAME,
    model_dir=model_dir,
    validation_metrics=validation_metrics,
    test_metrics=test_metrics,
    input_example=X_train.head(10),
    training_dataset_version=training_dataset_version,
)
    
    print(
        "\nTraining pipeline completed successfully!"
    )
    

    return {
    "model": model,
    "validation_metrics": validation_metrics,
    "test_metrics": test_metrics,
    "model_path": model_dir,
    "training_dataset_version": training_dataset_version,
}


def main():

    train_pipeline(
        target=[
            "target_day1",
            "target_day2",
            "target_day3",
        ],
        training_dataset_version=1,
    )


if __name__ == "__main__":
    main()