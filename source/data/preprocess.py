"""Prepare NASA C-MAPSS FD001 data, with a deterministic demo fallback."""
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler

SOURCE = Path(__file__).resolve().parents[1]; DATA = SOURCE / "data"
# FD001 rows contain 21 sensor channels (s1 ... s21).
COLS = ["engine_id", "cycle", "setting1", "setting2", "setting3"] + [f"s{i}" for i in range(1, 22)]

def demo_raw():
    rng = np.random.default_rng(2026); rows = []
    for engine in range(1, 9):
        cycles = 90 + engine * 3
        for cycle in range(1, cycles + 1):
            drift = cycle / cycles
            sensors = [100 + 4 * drift + rng.normal(0, .8), 0.4 + 1.8 * drift + rng.normal(0, .08), 300 - 45 * drift + rng.normal(0, 3), 1500 + 40 * drift + rng.normal(0, 9), 30 + 90 * drift + rng.normal(0, 4), 82 + 25 * drift + rng.normal(0, 2)] + list(rng.normal(0, 1, 17))
            rows.append([engine, cycle, 0.1, 0.2, 0.3] + sensors)
    return pd.DataFrame(rows, columns=COLS)

def preprocess():
    raw_path = DATA / "train_FD001.txt"
    if raw_path.exists(): df_raw = pd.read_csv(raw_path, sep=r"\s+", names=COLS)
    else: df_raw = demo_raw(); print("未发现 NASA 原始文件，已生成可演示的 C-MAPSS 风格样本。")
    df_raw["RUL"] = df_raw.groupby("engine_id")["cycle"].transform("max") - df_raw["cycle"]
    df_raw["fault_label"] = (df_raw["RUL"] <= 30).astype(int)
    df = df_raw.drop(columns=["setting3", "s1", "s5", "s10", "s16", "s18", "s19"], errors="ignore").copy()
    sensor_cols = [c for c in df.columns if c.startswith("s")]
    df[sensor_cols] = StandardScaler().fit_transform(df[sensor_cols])
    out = DATA / "processed_industrial_data.csv"; df.to_csv(out, index=False, encoding="utf-8")
    print(f"预处理完成: {out} | 样本 {len(df)} | 风险样本 {int(df.fault_label.sum())}")
    return df

if __name__ == "__main__": preprocess()
