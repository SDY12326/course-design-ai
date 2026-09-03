from fastapi import FastAPI
from pydantic import BaseModel
import numpy as np
from train import FaultLSTM
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

model = FaultLSTM()
#优先加载本地模型；没有就自动训练一套模拟模型
try:
    model.load_model()
    print("本地模型加载成功")
except Exception as e:
    print(f"未检测到模型文件，执行模拟训练:{e}")
    from train import get_demo_sample
    X_demo,y_demo = get_demo_sample()
    model.train(X_demo,y_demo)
    model.save_model()
    print("模拟演示模型训练完成并保存")


class Item(BaseModel):
    seq: list

@app.post("/predict")
async def predict(item:Item):
    arr = np.array(item.seq).reshape(1,-1)
    res = model.predict(arr)
    label_text = "故障预警" if res ==1 else "运行正常"
    return {"code":0,"result":res,"desc":label_text}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app,host="127.0.0.1",port=8000)
