-- 智维引擎业务数据库结构
CREATE TABLE IF NOT EXISTS equipment (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    line TEXT,
    status TEXT,
    last_seen TEXT,
    health REAL
);

CREATE TABLE IF NOT EXISTS sensor_readings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    equipment_id TEXT,
    recorded_at TEXT,
    payload TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS predictions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    equipment_id TEXT,
    created_at TEXT,
    payload TEXT NOT NULL
);
