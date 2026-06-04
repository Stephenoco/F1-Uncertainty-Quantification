import torch.nn as nn

class PitStrategyNet(nn.Module):
    def __init__(self, input_dim, hidden_dim_1=64, hidden_dim_2=32, dropout_rate=0.3):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(input_dim, hidden_dim_1),
            nn.ReLU(),
            nn.Dropout(dropout_rate),
            nn.Linear(hidden_dim_1, hidden_dim_1),  # extra layer
            nn.ReLU(),
            nn.Dropout(dropout_rate),
            nn.Linear(hidden_dim_1, hidden_dim_2),
            nn.ReLU(),
            nn.Dropout(dropout_rate),
            nn.Linear(hidden_dim_2, 1)
        )

    def forward(self, x):
        return self.net(x)