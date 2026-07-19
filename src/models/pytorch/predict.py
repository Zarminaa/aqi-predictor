import torch
import numpy as np


def predict(
    model,
    dataloader,
    device,
):

    model.eval()

    predictions = []

    with torch.no_grad():

        for batch in dataloader:

            X = batch[0].to(device)

            outputs = model(X)

            predictions.extend(
                outputs.cpu().numpy().flatten()
            )

    return np.array(predictions)