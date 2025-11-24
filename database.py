import sqlite3
from datetime import datetime
import uuid

DB_NAME = "chat_history_v2.db"

def init_db():
    """Veritabanini ve tablolari olusturur"""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    
    # Sessions tablosu (Sohbet Oturumlari)
    c.execute('''
        CREATE TABLE IF NOT EXISTS sessions (
            id TEXT PRIMARY KEY,
            title TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Messages tablosu (Mesajlar)
    c.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT,
            role TEXT NOT NULL,
            content TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(session_id) REFERENCES sessions(id)
        )
    ''')
    conn.commit()
    conn.close()

def create_session(title="New Chat"):
    """Yeni bir sohbet oturumu acar"""
    session_id = str(uuid.uuid4())
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('INSERT INTO sessions (id, title) VALUES (?, ?)', (session_id, title))
    conn.commit()
    conn.close()
    return session_id

def get_all_sessions():
    """Tum sohbet oturumlarini getirir (En yeniden eskiye)"""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('SELECT id, title FROM sessions ORDER BY created_at DESC')
    rows = c.fetchall()
    conn.close()
    return [{"id": row[0], "title": row[1]} for row in rows]

def save_message(session_id, role, content):
    """Belirli bir oturuma mesaj kaydeder"""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('INSERT INTO messages (session_id, role, content) VALUES (?, ?, ?)', (session_id, role, content))
    
    # Eger bu ilk mesajsa, oturum basligini guncelle (Opsiyonel: Ilk mesajin ilk 30 karakteri)
    if role == "user":
        c.execute('SELECT count(*) FROM messages WHERE session_id = ?', (session_id,))
        count = c.fetchone()[0]
        if count <= 2: # Ilk soru-cevap cifti
            new_title = content[:30] + "..." if len(content) > 30 else content
            c.execute('UPDATE sessions SET title = ? WHERE id = ?', (new_title, session_id))
            
    conn.commit()
    conn.close()

def get_messages(session_id):
    """Bir oturuma ait mesajlari getirir"""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('SELECT role, content FROM messages WHERE session_id = ? ORDER BY timestamp ASC', (session_id,))
    rows = c.fetchall()
    conn.close()
    return [{"role": row[0], "content": row[1]} for row in rows]

def delete_session(session_id):
    """Bir oturumu ve mesajlarini siler"""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('DELETE FROM messages WHERE session_id = ?', (session_id,))
    c.execute('DELETE FROM sessions WHERE id = ?', (session_id,))
    conn.commit()
    conn.close()
