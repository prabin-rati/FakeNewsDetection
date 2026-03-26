import sqlite3

conn = sqlite3.connect('users.db')
cursor = conn.cursor()

# Delete old tables
cursor.execute('DROP TABLE IF EXISTS users')
cursor.execute('DROP TABLE IF EXISTS history')

# Create Users Table
cursor.execute('''
    CREATE TABLE users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        username TEXT UNIQUE NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        role TEXT DEFAULT 'user'
    )
''')

# Create History Table
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
print("✅ Database Reset Successful!")