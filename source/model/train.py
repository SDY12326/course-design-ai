"""Train the supervised risk classifier used by the live API."""
from pathlib import Path
import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

SOURCE = Path(__file__).resolve().parents[1]
ROOT = SOURCE.parent
ARTIFACT = SOURCE / "model" / "risk_classifier.joblib"

def make_dataset(n_normal=None, n_risk=None):
    processed = SOURCE / "data" / "processed_industrial_data.csv"
    if n_normal is None and n_risk is None and processed.exists():
        df = pd.read_csv(processed)
        get = lambda key, default=0: df[key].fillna(default).to_numpy() if key in df else np.full(len(df), default)
        X = np.column_stack([71 + get("s2") * 5, 1.9 + np.abs(get("s3")) * .65, 305 + get("s4") * 18, 1500 + get("s6") * 25, np.maximum(0, 45 + get("s7") * 18), 93 + get("s8") * 7])
        return np.nan_to_num(X), df["fault_label"].to_numpy(dtype=int)
    n_normal = n_normal or 1200; n_risk = n_risk or 800
    rng = np.random.default_rng(2026)
    normal = np.column_stack([rng.normal(71, 5, n_normal), rng.normal(1.9, .55, n_normal), rng.normal(305, 18, n_normal), rng.normal(1500, 25, n_normal), rng.normal(42, 18, n_normal), rng.normal(93, 7, n_normal)])
    risk = np.column_stack([rng.normal(91, 7, n_risk), rng.normal(4.2, .8, n_risk), rng.normal(232, 22, n_risk), rng.normal(1570, 38, n_risk), rng.normal(118, 22, n_risk), rng.normal(119, 10, n_risk)])
    return np.vstack([normal, risk]), np.array([0] * n_normal + [1] * n_risk)

def train():
    X, y = make_dataset(); X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=.2, random_state=42, stratify=y)
    model = RandomForestClassifier(n_estimators=80, max_depth=8, random_state=42, class_weight="balanced")
    model.fit(X_train, y_train); pred = model.predict(X_val)
    metrics = {"accuracy": accuracy_score(y_val, pred), "precision": precision_score(y_val, pred), "recall": recall_score(y_val, pred), "f1": f1_score(y_val, pred)}
    ARTIFACT.parent.mkdir(exist_ok=True); joblib.dump(model, ARTIFACT)
    print(f"模型已保存: {ARTIFACT}"); print("验证集指标:", ", ".join(f"{k}={v:.4f}" for k, v in metrics.items()))
    return metrics

if __name__ == "__main__": train()
