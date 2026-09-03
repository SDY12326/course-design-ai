import os
import joblib
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler

class FaultLSTM:
    def __init__(self):
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.scaler = StandardScaler()
        self.model_path = "./model.pkl"
        self.scaler_path = "./scaler.pkl"

    def train(self, X_train, y_train):
        X_scaled = self.scaler.fit_transform(X_train)
        self.model.fit(X_scaled, y_train)

    def predict(self, x_input):
        x_scaled = self.scaler.transform(x_input)
        pred = self.model.predict(x_scaled)
        return int(pred[0])

    def save_model(self):
        joblib.dump(self.model, self.model_path)
        joblib.dump(self.scaler, self.scaler_path)

    def load_model(self):
        self.model = joblib.load(self.model_path)
        self.scaler = joblib.load(self.scaler_path)


def get_demo_sample():
    """模拟演示样本，无真实数据集也能跑通接口演示"""
    np.random.seed(2026)
    X = np.random.rand(200,50)
    y = np.random.randint(0,2,size=200)
    return X,y


if __name__ == "__main__":
    print("生成模拟演示数据集，开始训练模型……")
    X,y = get_demo_sample()
    obj = FaultLSTM()
    obj.train(X,y)
    obj.save_model()
    print("训练完成，model.pkl、scaler.pkl 已保存至backend目录")
  
