import sqlite3
import datetime
import pandas as pd

DB_PATH = "inventory.db"

def get_conn():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_conn()
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS inventory_current (
        item_name TEXT PRIMARY KEY,
        stock_count INTEGER,
        last_updated TEXT
    )""")
    c.execute("""
    CREATE TABLE IF NOT EXISTS inventory_log (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT,
        image_id TEXT,
        item_name TEXT,
        count INTEGER
    )""")
    conn.commit()
    conn.close()

def save_detection_to_db(image_id, counts):
    ts = datetime.datetime.utcnow().isoformat()
    conn = get_conn()
    c = conn.cursor()
    for item, count in counts.items():
        c.execute("INSERT INTO inventory_log (timestamp, image_id, item_name, count) VALUES (?,?,?,?)",
                  (ts, image_id, item, count))
        c.execute("INSERT OR REPLACE INTO inventory_current (item_name, stock_count, last_updated) VALUES (?,?,?)",
                  (item, count, ts))
    conn.commit()
    conn.close()

def get_current_inventory_df():
    conn = get_conn()
    df = pd.read_sql_query("SELECT * FROM inventory_current", conn)
    conn.close()
    return df

def get_inventory_log_df(limit=500):
    conn = get_conn()
    df = pd.read_sql_query(f"SELECT * FROM inventory_log ORDER BY timestamp DESC LIMIT {limit}", conn)
    conn.close()
    return df
