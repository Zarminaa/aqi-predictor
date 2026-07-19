import torch.nn as nn

from .config import (
    HIDDEN_1,
    HIDDEN_2,
    HIDDEN_3,
    DROPOUT,
)


class AQINetwork(nn.Module):

    def __init__(self, input_size):

        super().__init__()

        self.network = nn.Sequential(

            nn.Linear(input_size, HIDDEN_1),
            nn.ReLU(),
            nn.Dropout(DROPOUT),

            nn.Linear(HIDDEN_1, HIDDEN_2),
            nn.ReLU(),
            nn.Dropout(DROPOUT),

            nn.Linear(HIDDEN_2, HIDDEN_3),
            nn.ReLU(),

            nn.Linear(HIDDEN_3, 1),
        )

    def forward(self, x):

        return self.network(x)