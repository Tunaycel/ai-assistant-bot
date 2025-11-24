import sqlite3
from datetime import datetime

DB_NAME = "chat_history.db"

def init_db():
    """Veritabanini ve tablolari olusturur"""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            role TEXT NOT NULL,
            content TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def save_message(role, content):
    """Yeni bir mesaji veritabanina kaydeder"""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('INSERT INTO messages (role, content) VALUES (?, ?)', (role, content))
    conn.commit()
    conn.close()

def get_history():
    """Tum sohbet gecmisini getirir"""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('SELECT role, content FROM messages ORDER BY timestamp ASC')
    rows = c.fetchall()
    conn.close()
    # Streamlit formatina uygun liste dondur
    return [{"role": row[0], "content": row[1]} for row in rows]

def clear_history():
    """Tum gecmisi siler"""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('DELETE FROM messages')
    conn.commit()
    conn.close()
