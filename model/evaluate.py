"""
工业设备故障预测模型评估脚本
"""
import torch
import torch.nn as nn
from torch.utils.data import DataLoader
import pandas as pd
from sklearn.metrics import accuracy_score, f1_score, recall_score, precision_score, confusion_matrix
from train import val_loader, FaultLSTM, input_feature_dim, device

model = FaultLSTM(input_feature_dim).to(device)
model.load_state_dict(torch.load("./model/fault_lstm.pt"))
model.eval()

y_true = []
y_pred = []

with torch.no_grad():
    for x, y in val_loader:
        x, y = x.to(device), y.to(device)
        out = model(x).squeeze()
        pred_label = (out > 0.5).long()
        y_true.extend(y.cpu().numpy())
        y_pred.extend(pred_label.cpu().numpy())

acc = accuracy_score(y_true, y_pred)
pre = precision_score(y_true, y_pred)
rec = recall_score(y_true, y_pred)
f1 = f1_score(y_true, y_pred)
cm = confusion_matrix(y_true, y_pred)

print("====设备故障预测模型评估结果====")
print(f"准确率Accuracy:{acc:.4f}")
print(f"精确率Precision:{pre:.4f}")
print(f"召回率Recall:{rec:.4f}")
print(f"F1分数:{f1:.4f}")
print("混淆矩阵：")
print(cm)

#输出评估结果写入logs
with open("../logs/eval_result.txt","w",encoding="utf-8") as f:
    f.write(f"准确率Accuracy:{acc:.4f}\n")
    f.write(f"精确率Precision:{pre:.4f}\n")
    f.write(f"召回率Recall:{rec:.4f}\n")
    f.write(f"F1分数:{f1:.4f}\n")
    f.write(f"混淆矩阵:\n{cm}")
