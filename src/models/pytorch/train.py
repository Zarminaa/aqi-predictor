import copy

import torch
import torch.nn as nn
from torch.optim import Adam

from src.models.pytorch.evaluate import evaluate_model

from .config import (
    EPOCHS,
    LEARNING_RATE,
)
from .model import AQINetwork


def train_pytorch(
    train_loader,
    val_loader,
    y_val,
    input_size,
    output_size,
):

    device = torch.device(
        "cuda"
        if torch.cuda.is_available()
        else "cpu"
    )

    model = AQINetwork(
        input_size=input_size,
        output_size=output_size,
    ).to(device)

    criterion = nn.MSELoss()

    optimizer = Adam(
        model.parameters(),
        lr=LEARNING_RATE,
    )

    best_r2 = float("-inf")
    best_model = None

    for epoch in range(EPOCHS):

        model.train()

        epoch_loss = 0

        for X_batch, y_batch in train_loader:

            X_batch = X_batch.to(device)
            y_batch = y_batch.to(device)

            optimizer.zero_grad()

            predictions = model(X_batch)

            loss = criterion(
                predictions,
                y_batch,
            )

            loss.backward()

            optimizer.step()

            epoch_loss += loss.item()

        print(
            f"Epoch {epoch+1:03d}/{EPOCHS} "
            f"Loss: {epoch_loss / len(train_loader):.4f}"
        )

        # ------------------------------------------
        # Evaluate every 10 epochs
        # ------------------------------------------
        if (epoch + 1) % 10 == 0:

            print("\nValidation Results")

            metrics = evaluate_model(
                model=model,
                dataloader=val_loader,
                y_true=y_val,
                device=device,
            )

            current_r2 = metrics["Overall"]["R2"]

            print(
                f"Validation Overall R²: "
                f"{current_r2:.4f}"
            )

            if current_r2 > best_r2:

                best_r2 = current_r2
                best_model = copy.deepcopy(model)

                print("✓ New best model saved")

    # ------------------------------------------
    # Restore best model
    # ------------------------------------------
    if best_model is not None:

        model = best_model

    print("\n" + "=" * 50)
    print(f"Best Validation R²: {best_r2:.4f}")
    print("=" * 50)

    return model, device