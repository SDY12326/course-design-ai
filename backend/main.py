"""
FastAPI后端服务：工业设备故障预警接口
接收传感器时序数据，调用训练好的LSTM模型，返回故障预警结果
"""
from fastapi import FastAPI
import torch
import numpy as np
import sys
sys.path.append("../model")
from train import FaultLSTM

app = FastAPI(title="设备故障预警接口")

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
#加载训练完成模型
model = FaultLSTM(input_dim=13).to(device)
model.load_state_dict(torch.load("../model/fault_lstm.pt",map_location=device))
model.eval()

@app.post("/predict")
def predict_fault(sensor_seq:list):
    """
    sensor_seq:50步传感器时序输入
    return: fault_prob故障概率，is_risk 是否故障风险
    """
    input_tensor = torch.tensor([sensor_seq],dtype=torch.float32).to(device)
    with torch.no_grad():
        prob = model(input_tensor).item()
    risk_flag = 1 if prob>0.5 else 0
    return {
        "fault_probability":round(prob,4),
        "is_fault_risk":risk_flag
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app,host="0.0.0.0",port=8000)
