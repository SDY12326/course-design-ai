"""Deterministic, explainable algorithms used by the classroom demo."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Any
import math
import numpy as np
from pathlib import Path

try:
    from sklearn.ensemble import RandomForestClassifier
except ImportError:  # pragma: no cover - requirements installs sklearn in normal runs
    RandomForestClassifier = None

SENSOR_META = {
    "temperature": {"label": "轴承温度", "unit": "°C", "normal": (60, 82), "warn": 90, "direction": 1},
    "vibration": {"label": "振动幅值", "unit": "mm/s", "normal": (0, 3.2), "warn": 4.5, "direction": 1},
    "pressure": {"label": "润滑油压力", "unit": "kPa", "normal": (260, 330), "warn": 220, "direction": -1},
    "rpm": {"label": "主轴转速", "unit": "rpm", "normal": (1450, 1550), "warn": 1600, "direction": 1},
    "oil_quality": {"label": "油液污染度", "unit": "ppm", "normal": (0, 80), "warn": 120, "direction": 1},
    "power": {"label": "单位能耗", "unit": "kW", "normal": (80, 105), "warn": 120, "direction": 1},
}

@dataclass
class Diagnosis:
    risk_score: float
    is_risk: bool
    rul_hours: int
    anomaly_score: float
    anomaly_sensors: list[dict[str, Any]]
    recommendation: str
    model_name: str = "融合风险模型 v1"

def preprocess(values: dict[str, float]) -> dict[str, float]:
    clean = {}
    for key, meta in SENSOR_META.items():
        try: value = float(values.get(key, sum(meta["normal"]) / 2))
        except (TypeError, ValueError): value = sum(meta["normal"]) / 2
        if not math.isfinite(value): value = sum(meta["normal"]) / 2
        low, high = meta["normal"]
        clean[key] = round(float(np.clip(value, low - (high - low) * 2, high + (high - low) * 2)), 3)
    return clean

def _severity(key: str, value: float) -> float:
    meta = SENSOR_META[key]; low, high = meta["normal"]
    if meta["direction"] > 0: return max(0.0, (value - high) / max(meta["warn"] - high, 1e-6))
    return max(0.0, (low - value) / max(low - meta["warn"], 1e-6))

def _train_classifier():
    """Train a tiny deterministic classifier for the live demo.

    The training data represents normal/risk operating envelopes. A real C-MAPSS
    export can replace this fixture without changing the API feature contract.
    """
    if RandomForestClassifier is None:
        return None
    X, y = _training_data()
    model = RandomForestClassifier(n_estimators=80, max_depth=8, random_state=42, class_weight="balanced")
    model.fit(X, y)
    return model

def _training_data():
    """Prefer processed NASA FD001 rows; use fixtures only for an empty checkout."""
    source = Path(__file__).resolve().parents[1]
    path = source / "data" / "processed_industrial_data.csv"
    if path.exists():
        import pandas as pd
        df = pd.read_csv(path)
        get = lambda key, default=0: df[key].fillna(default).to_numpy() if key in df else np.full(len(df), default)
        X = np.column_stack([71 + get("s2") * 5, 1.9 + np.abs(get("s3")) * .65, 305 + get("s4") * 18, 1500 + get("s6") * 25, np.maximum(0, 45 + get("s7") * 18), 93 + get("s8") * 7])
        return np.nan_to_num(X), df["fault_label"].to_numpy(dtype=int)
    rng = np.random.default_rng(2026)
    normal = np.column_stack([rng.normal(71, 5, 1200), rng.normal(1.9, .55, 1200), rng.normal(305, 18, 1200), rng.normal(1500, 25, 1200), rng.normal(42, 18, 1200), rng.normal(93, 7, 1200)])
    risk = np.column_stack([rng.normal(91, 7, 800), rng.normal(4.2, .8, 800), rng.normal(232, 22, 800), rng.normal(1570, 38, 800), rng.normal(118, 22, 800), rng.normal(119, 10, 800)])
    return np.vstack([normal, risk]), np.array([0] * len(normal) + [1] * len(risk))

CLASSIFIER = _train_classifier()

def diagnose(values: dict[str, float], history: list[dict[str, float]] | None = None) -> Diagnosis:
    clean = preprocess(values)
    severities = {key: min(1.0, _severity(key, val)) for key, val in clean.items()}
    weights = {"temperature": .22, "vibration": .25, "pressure": .18, "rpm": .1, "oil_quality": .15, "power": .1}
    rule_score = min(0.99, max(0.01, sum(severities[k] * weights[k] for k in weights) + .03))
    model_score = None
    if CLASSIFIER is not None:
        model_score = float(CLASSIFIER.predict_proba([[clean[k] for k in SENSOR_META]])[0, 1])
    risk_score = model_score * .65 + rule_score * .35 if model_score is not None else rule_score
    if history and len(history) >= 4:
        baseline = {k: np.mean([float(row.get(k, clean[k])) for row in history[-20:]]) for k in clean}
        spread = {k: max(np.std([float(row.get(k, clean[k])) for row in history[-20:]]), .1) for k in clean}
    else:
        baseline = {k: sum(SENSOR_META[k]["normal"]) / 2 for k in clean}
        spread = {k: max((SENSOR_META[k]["normal"][1] - SENSOR_META[k]["normal"][0]) / 4, .1) for k in clean}
    anomalies, z_values = [], []
    for key, value in clean.items():
        z = abs((value - baseline[key]) / spread[key]); z_values.append(z)
        if z >= 2.0 or severities[key] >= .65:
            anomalies.append({"key": key, "label": SENSOR_META[key]["label"], "value": value, "unit": SENSOR_META[key]["unit"], "z_score": round(float(z), 2), "severity": round(float(min(1, max(z / 4, severities[key]))), 2)})
    anomaly_score = min(0.99, float(np.mean(np.minimum(np.array(z_values) / 4, 1)))) if z_values else 0
    risk_score = min(.99, risk_score * .72 + anomaly_score * .28)
    is_risk = risk_score >= .5 or len(anomalies) >= 2
    rul = int(max(8, min(720, 720 * (1 - risk_score) * (1 - .35 * anomaly_score))))
    if is_risk:
        top = anomalies[0]["label"] if anomalies else "关键传感器"
        recommendation = f"建议在 {max(2, min(24, rul // 12))} 小时内安排点检，优先检查{top}并复核润滑与负载。"
    else: recommendation = "设备处于可控区间，建议维持当前巡检周期并持续采集时序数据。"
    model_name = "RandomForest风险分类 + z-score异常检测"
    return Diagnosis(round(risk_score, 4), is_risk, rul, round(anomaly_score, 4), anomalies, recommendation, model_name)

def trend(history: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [{"time": row["time"], "risk_score": row["risk_score"], "temperature": row["temperature"], "vibration": row["vibration"]} for row in history[-24:]]
