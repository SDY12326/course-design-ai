"""
工业设备故障预测LSTM模型训练脚本
NASA C-MAPSS涡轮发动机数据集，二分类故障预警
"""
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
import pandas as pd
import numpy as np
import os

# ==================== 配置参数 ====================
SEQ_LEN = 50
BATCH_SIZE = 16
HIDDEN_DIM = 128
LEARNING_RATE = 1e-3
NUM_EPOCHS = 6
TRAIN_RATIO = 0.8
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# ==================== 数据集定义 ====================
class EngineDataset(Dataset):
    def __init__(self, sequences, labels):
        self.sequences = sequences
        self.labels = labels

    def __len__(self):
        return len(self.sequences)

    def __getitem__(self, idx):
        return (
            torch.tensor(self.sequences[idx], dtype=torch.float32),
            torch.tensor(self.labels[idx], dtype=torch.float32),
        )

def build_sequences(df, sensor_cols, seq_len=50):
    sequences, labels = [], []
    for engine_id in df["engine_id"].unique():
        engine_data = df[df["engine_id"] == engine_id].sort_values("cycle")
        sensor_values = engine_data[sensor_cols].values
        fault_values = engine_data["fault_label"].values
        for i in range(len(sensor_values) - seq_len + 1):
            sequences.append(sensor_values[i : i + seq_len])
            labels.append(fault_values[i + seq_len - 1])
    return np.array(sequences), np.array(labels)

# ==================== 模型定义 ====================
class FaultLSTM(nn.Module):
    def __init__(self, input_dim, hidden_dim=128):
        super(FaultLSTM, self).__init__()
        self.lstm = nn.LSTM(input_dim, hidden_dim, batch_first=True)
        self.fc = nn.Linear(hidden_dim, 1)
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        out, _ = self.lstm(x)
        out = out[:, -1, :]
        out = self.fc(out)
        out = self.sigmoid(out)
        return out

# ==================== 主训练流程 ====================
if __name__ == "__main__":
    df = pd.read_csv("./data/processed_industrial_data.csv")
    sensor_cols = [col for col in df.columns if col.startswith("s")]
    input_feature_dim = len(sensor_cols)
    print(f"传感器特征数: {input_feature_dim}")

    X, y = build_sequences(df, sensor_cols, SEQ_LEN)
    print(f"序列样本总数: {len(X)}, 故障样本占比: {y.mean():.3f}")

    engine_ids = df["engine_id"].unique()
    np.random.seed(42)
    np.random.shuffle(engine_ids)
    split_idx = int(len(engine_ids) * TRAIN_RATIO)
    train_engines = set(engine_ids[:split_idx])

    train_mask = df["engine_id"].isin(train_engines).values
    train_indices = []
    val_indices = []
    for i, engine_id in enumerate(df["engine_id"].unique()):
        engine_data = df[df["engine_id"] == engine_id].sort_values("cycle")
        n_samples = len(engine_data) - SEQ_LEN + 1
        start = i * (df["engine_id"].value_counts().sort_index().values[i] - SEQ_LEN + 1)
        indices = list(range(start, start + n_samples))
        if engine_id in train_engines:
            train_indices.extend(indices)
        else:
            val_indices.extend(indices)

    train_dataset = EngineDataset(X[train_indices], y[train_indices])
    val_dataset = EngineDataset(X[val_indices], y[val_indices])

    train_loader = DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=BATCH_SIZE, shuffle=False)

    model = FaultLSTM(input_feature_dim, HIDDEN_DIM).to(DEVICE)
    criterion = nn.BCELoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=LEARNING_RATE)

    print(f"训练集样本: {len(train_dataset)}, 验证集样本: {len(val_dataset)}")
    print(f"设备: {DEVICE}, 开始训练...")

    for epoch in range(NUM_EPOCHS):
        model.train()
        train_loss = 0.0
        for x_batch, y_batch in train_loader:
            x_batch, y_batch = x_batch.to(DEVICE), y_batch.to(DEVICE).unsqueeze(1)
            optimizer.zero_grad()
            outputs = model(x_batch)
            loss = criterion(outputs, y_batch)
            loss.backward()
            optimizer.step()
            train_loss += loss.item()

        model.eval()
        val_loss = 0.0
        with torch.no_grad():
            for x_batch, y_batch in val_loader:
                x_batch, y_batch = x_batch.to(DEVICE), y_batch.to(DEVICE).unsqueeze(1)
                outputs = model(x_batch)
                val_loss += criterion(outputs, y_batch).item()

        print(f"Epoch {epoch+1}/{NUM_EPOCHS} | "
              f"Train Loss: {train_loss/len(train_loader):.4f} | "
              f"Val Loss: {val_loss/len(val_loader):.4f}")

    os.makedirs("./model", exist_ok=True)
    torch.save(model.state_dict(), "./model/fault_lstm.pt")
    print("训练完成，模型已保存至 model/fault_lstm.pt")
