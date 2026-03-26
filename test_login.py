import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

# 1. Create a test user manually
conn = sqlite3.connect('users.db')
cursor = conn.cursor()
hashed = generate_password_hash('bca123')
try:
    cursor.execute("INSERT INTO users (username, password, email) VALUES (?, ?, ?)", 
                   ('bcatest', hashed, 'test@tu.edu.np'))
    conn.commit()
    print("✅ Test user 'bcatest' created with password 'bca123'")
except:
    print("⚠️ User already exists, proceeding to check...")

# 2. Try to 'Login' manually
user = cursor.execute("SELECT password FROM users WHERE username='bcatest'").fetchone()
if user and check_password_hash(user[0], 'bca123'):
    print("✅ SUCCESS: The Password Logic is working!")
else:
    print("❌ FAIL: The Password Logic is broken!")
conn.close()