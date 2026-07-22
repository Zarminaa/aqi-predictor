from src.data.load_data import load_features
from src.data.split_data import split_data
from sklearn.preprocessing import StandardScaler
from src.models.pytorch.save_scaler import save_scaler
from src.models.pytorch.dataset import create_dataloader
from src.models.pytorch.train import train_pytorch
from src.models.pytorch.evaluate import evaluate_model
from src.models.pytorch.save_model import save_model


def train_pipeline(target):
    """
    PyTorch training pipeline.
    """

    print("=" * 60)
    print("PYTORCH TRAINING PIPELINE")
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


     # ----------------------------------------------------
    # Feature Scaling
    # ----------------------------------------------------
    print("\nScaling features...")

    scaler = StandardScaler()

    X_train = scaler.fit_transform(X_train)
    save_scaler(
    scaler,
    filename=f"pytorch_{target}_scaler.pkl",
)

    X_val = scaler.transform(X_val)

    X_test = scaler.transform(X_test)

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
    # Train Model
    # ----------------------------------------------------
    print("\nTraining PyTorch Model...")

    model, device = train_pytorch(
        train_loader=train_loader,
        input_size=X_train.shape[1],
    )

    print("Training completed!")

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

    # ----------------------------------------------------
    # Save Model
    # ----------------------------------------------------
    print("\nSaving model...")

    filename = f"pytorch_{target}.pt"

    save_model(
        model=model,
        filename=filename,
    )

    print("\nTraining pipeline completed successfully!")

    return {
        "model": model,
        "validation_metrics": validation_metrics,
        "test_metrics": test_metrics,
    }


def main():

    train_pipeline(
        target="target_day1",
    )


if __name__ == "__main__":
    main()