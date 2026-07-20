import numpy as np
import torch
from torch.utils.data import TensorDataset, DataLoader

from .config import BATCH_SIZE


def create_dataloader(
    X,
    y=None,
    shuffle=False,
):

    X = torch.tensor(
        np.asarray(X),
        dtype=torch.float32,
    )

    if y is not None:

        y = torch.tensor(
            np.asarray(y),
            dtype=torch.float32,
        ).view(-1, 1)

        dataset = TensorDataset(
            X,
            y,
        )

    else:

        dataset = TensorDataset(X)

    return DataLoader(
        dataset,
        batch_size=BATCH_SIZE,
        shuffle=shuffle,
    )