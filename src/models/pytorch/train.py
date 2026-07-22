import torch
import torch.nn as nn

from torch.optim import Adam

from .model import AQINetwork
from .config import (
    LEARNING_RATE,
    EPOCHS,
)


def train_pytorch(
    train_loader,
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
            f"Loss: {epoch_loss/len(train_loader):.4f}"
        )

    return model, device