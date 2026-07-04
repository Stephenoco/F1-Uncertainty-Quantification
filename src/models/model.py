import torch
import torch.nn as nn

class PitStrategyNet(nn.Module):
    def __init__(self, input_dim, hidden_dim_1=64, hidden_dim_2=32, dropout_rate=0.3, num_classes=3):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(input_dim, hidden_dim_1),
            nn.ReLU(),
            nn.Dropout(dropout_rate),
            nn.Linear(hidden_dim_1, hidden_dim_2),
            nn.ReLU(),
            nn.Dropout(dropout_rate),
            nn.Linear(hidden_dim_2, num_classes)
        )

    def forward(self, x):
        return self.net(x)

class PitStrategyLSTM(nn.Module):
    def __init__(self, input_dim, hidden_dim=64, num_layers=2, num_classes= 3, dropout_rate=0.3):
        super().__init__()
        self.lstm = nn.LSTM(
            input_size  = input_dim,
            hidden_size = hidden_dim,
            num_layers  = num_layers,
            batch_first = True,
            dropout     = dropout_rate if num_layers > 1 else 0.0
        )
        self.dropout = nn.Dropout(dropout_rate)
        self.fc = nn.Linear(hidden_dim, num_classes)

    def forward(self, x):
        out, _ = self.lstm(x)
        out = self.dropout(out[:, -1, :])  # take last timestep only
        return self.fc(out)

class PitStrategyGRUAttention(nn.Module):
    def __init__(self, input_dim, hidden_dim=64, num_layers=2, dropout_rate=0.3, num_classes=3):
        super().__init__()
        self.gru = nn.GRU(
            input_size=input_dim,
            hidden_size=hidden_dim,
            num_layers=num_layers,
            batch_first=True,
            dropout=dropout_rate if num_layers > 1 else 0.0
        )
        self.attention = nn.Linear(hidden_dim, 1)
        self.dropout = nn.Dropout(dropout_rate)
        self.fc = nn.Linear(hidden_dim, num_classes)

    def forward(self, x):
        out, _ = self.gru(x)
        attn_weights = torch.softmax(self.attention(out), dim=1)
        context = (attn_weights * out).sum(dim=1)
        context = self.dropout(context)
        return self.fc(context)