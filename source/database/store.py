"""SQLite persistence and deterministic demo fixtures."""
from __future__ import annotations
import json, random, sqlite3
from pathlib import Path
from datetime import datetime, timedelta

SOURCE = Path(__file__).resolve().parents[1]
DB_PATH = SOURCE / "database" / "engine.db"
SCHEMA_PATH = SOURCE / "database" / "schema.sql"

def connect():
    conn = sqlite3.connect(DB_PATH); conn.row_factory = sqlite3.Row; return conn

def init_db():
    DB_PATH.parent.mkdir(exist_ok=True)
    with connect() as conn:
        conn.executescript(SCHEMA_PATH.read_text(encoding="utf-8"))
        if conn.execute("SELECT COUNT(*) FROM equipment").fetchone()[0] == 0: seed_demo(conn)

def seed_demo(conn):
    random.seed(2026); equipment = [("T-01", "1号涡轮压缩机", "A产线·动力段"), ("T-02", "2号涡轮压缩机", "A产线·动力段"), ("P-03", "冷却泵组 P-03", "B产线·冷却段"), ("M-07", "主轴电机 M-07", "B产线·装配段")]
    now = datetime.now().replace(second=0, microsecond=0)
    for idx, (eid, name, line) in enumerate(equipment):
        for n in range(24):
            phase = n / 23 + idx * .08
            payload = {"temperature": round(69 + idx * 2 + phase * (13 if idx == 1 else 4) + random.uniform(-1.4, 1.4), 2), "vibration": round(1.7 + idx * .25 + phase * (2.8 if idx == 1 else .5) + random.uniform(-.18, .18), 2), "pressure": round(306 - idx * 5 - phase * (58 if idx == 1 else 12) + random.uniform(-3, 3), 2), "rpm": round(1495 + random.uniform(-18, 18) + phase * (80 if idx == 3 else 10), 2), "oil_quality": round(38 + idx * 7 + phase * (92 if idx == 1 else 20) + random.uniform(-4, 4), 2), "power": round(91 + idx * 2 + phase * (29 if idx == 3 else 7) + random.uniform(-2, 2), 2)}
            conn.execute("INSERT INTO sensor_readings(equipment_id, recorded_at, payload) VALUES(?,?,?)", (eid, (now - timedelta(hours=23-n)).isoformat(timespec="minutes"), json.dumps(payload)))
        conn.execute("INSERT INTO equipment VALUES(?,?,?,?,?,?)", (eid, name, line, "预警" if idx == 1 else "运行中", now.isoformat(timespec="minutes"), 61 if idx == 1 else 92 - idx * 4))
    conn.commit()

def equipment_rows():
    with connect() as conn: return [dict(r) for r in conn.execute("SELECT * FROM equipment ORDER BY id")]

def latest_reading(eid):
    with connect() as conn:
        row = conn.execute("SELECT * FROM sensor_readings WHERE equipment_id=? ORDER BY id DESC LIMIT 1", (eid,)).fetchone()
        return {**dict(row), "payload": json.loads(row["payload"])} if row else None

def history(eid, limit=24):
    with connect() as conn:
        rows = conn.execute("SELECT recorded_at, payload FROM sensor_readings WHERE equipment_id=? ORDER BY id DESC LIMIT ?", (eid, limit)).fetchall()
        return [{"time": r["recorded_at"], **json.loads(r["payload"])} for r in reversed(rows)]

def save_prediction(eid, payload):
    with connect() as conn:
        conn.execute("INSERT INTO sensor_readings(equipment_id, recorded_at, payload) VALUES(?,?,?)", (eid, datetime.now().isoformat(timespec="minutes"), json.dumps(payload["sensors"], ensure_ascii=False)))
        conn.execute("INSERT INTO predictions(equipment_id, created_at, payload) VALUES(?,?,?)", (eid, datetime.now().isoformat(timespec="seconds"), json.dumps(payload, ensure_ascii=False)))
        conn.execute("UPDATE equipment SET health=?, status=?, last_seen=? WHERE id=?", (round((1-payload["risk_score"])*100, 1), "预警" if payload["is_risk"] else "运行中", datetime.now().isoformat(timespec="minutes"), eid))

def prediction_rows(limit=20):
    with connect() as conn:
        rows = conn.execute("SELECT id,equipment_id,created_at,payload FROM predictions ORDER BY id DESC LIMIT ?", (limit,)).fetchall()
        return [{**dict(r), "payload": json.loads(r["payload"])} for r in rows]
