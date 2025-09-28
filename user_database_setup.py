import sqlite3

conn = sqlite3.connect('users.db')
cursor = conn.cursor()

# Create a table for users with columns for physical measurements
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    age INTEGER,
    height REAL,
    weight REAL,
    blood_pressure TEXT
)
''')

conn.commit()
conn.close()

print("✅ User database and table created successfully.")