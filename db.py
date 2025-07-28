import sqlite3

# Connect to (or create) the database file
conn = sqlite3.connect('users.db')
cursor = conn.cursor()

# Create the users table
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    email TEXT PRIMARY KEY,
    username TEXT NOT NULL
)
''')

# Save (commit) the changes and close the connection
conn.commit()
conn.close()
