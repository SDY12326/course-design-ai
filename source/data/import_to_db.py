"""Load the processed C-MAPSS CSV into the application's SQLite sensor table.

Usage: ``python source/data/import_to_db.py`` from the repository root.
"""
import json, sqlite3
import sys
from datetime import datetime
from pathlib import Path
import pandas as pd

SOURCE = Path(__file__).resolve().parents[1]
ROOT = SOURCE.parent
sys.path.insert(0, str(SOURCE))
from database.store import init_db
DB = SOURCE / "database" / "engine.db"
CSV = SOURCE / "data" / "processed_industrial_data.csv"
ASSETS = ["T-01", "T-02", "P-03", "M-07"]

def to_payload(row):
    # Convert normalized C-MAPSS channels into the six dashboard engineering channels.
    vals = row.to_dict()
    get = lambda key, default=0: float(vals.get(key, default))
    return {"temperature": round(71 + get("s2") * 5, 2), "vibration": round(max(0, 1.9 + abs(get("s3")) * .65), 2), "pressure": round(305 + get("s4") * 18, 2), "rpm": round(1500 + get("s6") * 25, 2), "oil_quality": round(max(0, 45 + get("s7") * 18), 2), "power": round(93 + get("s8") * 7, 2)}

def import_csv():
    init_db()
    if not CSV.exists():
        from data.preprocess import preprocess
        preprocess()
    df = pd.read_csv(CSV)
    with sqlite3.connect(DB) as conn:
        conn.execute("DELETE FROM sensor_readings WHERE equipment_id IN (?,?,?,?)", tuple(ASSETS))
        for _, row in df.iterrows():
            eid = ASSETS[(int(row["engine_id"]) - 1) % len(ASSETS)]
            recorded = datetime.now().isoformat(timespec="minutes")
            conn.execute("INSERT INTO sensor_readings(equipment_id, recorded_at, payload) VALUES(?,?,?)", (eid, recorded, json.dumps(to_payload(row))))
    print(f"已将 {len(df)} 条处理后时序记录写入 {DB}")

if __name__ == "__main__": import_csv()
