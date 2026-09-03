# backend 目录说明
FastAPI 后端服务承载设备台账、诊断、CSV 导入和预测记录 API。

## 文件清单
1. main.py：服务入口，提供 `/api/equipment`、`/api/predict`、`/api/import`、`/api/predictions`
2. algorithms.py：清洗、融合风险分类、鲁棒异常检测与 RUL 估计

## 接口说明
- POST `/api/predict`
- 请求参数：`equipment_id` 与六项传感器数值
- 返回：`risk_score`、`is_risk`、`rul_hours`、`anomaly_sensors`、`recommendation`

## 运行方式
1. 安装依赖：fastapi、uvicorn、torch
2. 在项目根目录执行：`python source/backend/main.py`
3. 服务默认启动在 http://127.0.0.1:8000
4. 接口文档访问：http://127.0.0.1:8000/docs
