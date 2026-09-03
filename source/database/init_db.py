"""Initialize the project's SQLite database from ``schema.sql``."""
from pathlib import Path
import sqlite3

SOURCE = Path(__file__).resolve().parents[1]
DB_PATH = SOURCE / "database" / "engine.db"
SCHEMA_PATH = SOURCE / "database" / "schema.sql"

def init_table():
    DB_PATH.parent.mkdir(exist_ok=True)
    with sqlite3.connect(DB_PATH) as conn:
        conn.executescript(SCHEMA_PATH.read_text(encoding="utf-8"))

if __name__ == "__main__":
    init_table()
    print(f"数据库表初始化完成: {DB_PATH}")
