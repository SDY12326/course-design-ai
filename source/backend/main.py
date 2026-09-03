from __future__ import annotations
import csv, io
import sys
from pathlib import Path
from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
SOURCE = Path(__file__).resolve().parents[1]
ROOT = SOURCE.parent
sys.path.insert(0, str(SOURCE))
from backend.algorithms import SENSOR_META, diagnose, trend
from database.store import init_db, equipment_rows, latest_reading, history, save_prediction, prediction_rows

app = FastAPI(title="智维引擎·工业设备预测性维护", version="1.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

class PredictionRequest(BaseModel):
    equipment_id: str = Field("T-01", min_length=2)
    sensors: dict[str, float]

@app.on_event("startup")
def startup(): init_db()

@app.get("/", include_in_schema=False)
def index(): return FileResponse(SOURCE / "frontend" / "index.html")

@app.get("/api/health")
def health(): return {"status": "ok", "service": "predictive-maintenance", "algorithms": ["时序预处理", "融合风险分类", "鲁棒异常检测"]}

@app.get("/api/equipment")
def equipment():
    result = []
    for row in equipment_rows():
        reading = latest_reading(row["id"])
        result.append({**row, "latest": reading["payload"] if reading else {}})
    return result

@app.get("/api/equipment/{equipment_id}")
def equipment_detail(equipment_id: str):
    rows = [r for r in equipment_rows() if r["id"] == equipment_id]
    if not rows: raise HTTPException(404, "设备不存在")
    hist = history(equipment_id)
    return {**rows[0], "latest": hist[-1] if hist else {}, "trend": trend([{**row, "risk_score": 0} for row in hist])}

@app.post("/api/predict")
def predict(req: PredictionRequest):
    if req.equipment_id not in {r["id"] for r in equipment_rows()}: raise HTTPException(404, "设备不存在")
    result = diagnose(req.sensors, history(req.equipment_id))
    payload = {"risk_score": result.risk_score, "is_risk": result.is_risk, "rul_hours": result.rul_hours, "anomaly_score": result.anomaly_score, "anomaly_sensors": result.anomaly_sensors, "recommendation": result.recommendation, "model_name": result.model_name, "sensors": req.sensors}
    save_prediction(req.equipment_id, payload)
    return {"code": 0, "equipment_id": req.equipment_id, **payload}

@app.post("/api/import")
async def import_csv(file: UploadFile = File(...)):
    raw = await file.read()
    try: rows = list(csv.DictReader(io.StringIO(raw.decode("utf-8-sig"))))
    except Exception as exc: raise HTTPException(400, f"CSV解析失败: {exc}")
    required = {"equipment_id", *SENSOR_META.keys()}
    if not rows or not required.issubset(rows[0]): raise HTTPException(400, "CSV需包含 equipment_id 与六项传感器字段")
    accepted = 0
    for row in rows:
        try: predict(PredictionRequest(equipment_id=row["equipment_id"], sensors={k: float(row[k]) for k in SENSOR_META}))
        except (ValueError, TypeError, HTTPException): continue
        accepted += 1
    return {"code": 0, "accepted": accepted, "total": len(rows)}

@app.get("/api/predictions")
def predictions(): return prediction_rows()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=False)
