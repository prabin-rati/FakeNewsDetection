import sqlite3

conn = sqlite3.connect('users.db')
cursor = conn.cursor()
# Table to store history linked to a specific user_id
cursor.execute('''
    CREATE TABLE IF NOT EXISTS history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        news_text TEXT,
        result TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )
''')
conn.commit()
conn.close()
print("✅ History table added!")