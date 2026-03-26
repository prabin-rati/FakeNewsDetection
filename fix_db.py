import sqlite3

conn = sqlite3.connect('users.db')
cursor = conn.cursor()

# 1. Drop the old table if it's broken
cursor.execute('DROP TABLE IF EXISTS users')

# 2. Create the table with EXACT names matching app.py
cursor.execute('''
    CREATE TABLE users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name TEXT,
        last_name TEXT,
        username TEXT UNIQUE NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        role TEXT DEFAULT 'user'
    )
''')

# 3. Create the history table too just in case
cursor.execute('DROP TABLE IF EXISTS history')
cursor.execute('''
    CREATE TABLE history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        news_text TEXT,
        result TEXT,
        timestamp TEXT,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )
''')

conn.commit()
conn.close()
print("✅ Database repaired! All columns now match app.py.")