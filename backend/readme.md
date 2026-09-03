# backend目录说明
本文件夹存放FastAPI后端服务代码，为前端提供故障预测接口。

## 文件清单
1. main.py：后端主程序，提供/predict预测接口

## 接口说明
- POST /predict
- 请求参数：sensor_seq，长度为50的传感器时序列表
- 返回：fault_probability故障概率，is_fault_risk是否故障风险（1代表有风险）

## 运行方式
1. 安装依赖：fastapi、uvicorn、torch
2. 进入backend目录执行：python main.py
3. 服务默认启动在 http://127.0.0.1:8000
4. 接口文档访问：http://127.0.0.1:8000/docs
