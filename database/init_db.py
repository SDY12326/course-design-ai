"""
sqlite数据库初始化脚本
创建预测记录表，保存每次故障预测的输入与输出
"""
import sqlite3

def init_table():
    conn = sqlite3.connect("engine.db")
    cur = conn.cursor()
    cur.execute('''
    CREATE TABLE IF NOT EXISTS predict_log(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        input_seq TEXT,
        fault_prob REAL,
        is_risk INTEGER,
        create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_table()
    print("数据库表初始化完成")
