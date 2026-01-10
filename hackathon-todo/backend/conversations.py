import sqlite3

def init_db():
    conn = sqlite3.connect('conversations.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS conversations
                 (id TEXT, role TEXT, content TEXT, timestamp TEXT)''')
    conn.commit()
    conn.close()

init_db()

def save_message(conversation_id: str, role: str, content: str):
    conn = sqlite3.connect('conversations.db')
    c = conn.cursor()
    c.execute("INSERT INTO conversations VALUES (?, ?, ?, datetime('now'))",
              (conversation_id, role, content))
    conn.commit()
    conn.close()

def get_conversation(conversation_id: str):
    conn = sqlite3.connect('conversations.db')
    c = conn.cursor()
    c.execute("SELECT role, content FROM conversations WHERE id=? ORDER BY timestamp",
              (conversation_id,))
    messages = c.fetchall()
    conn.close()
    return messages