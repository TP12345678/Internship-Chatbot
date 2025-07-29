import sqlite3

def create_advanced_schema(db_path="backend/users.db"):
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()

            # User Table
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id TEXT PRIMARY KEY,
                username TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            );
            """)

            # Conversations Table
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                sub_question TEXT,
                response TEXT,
                FOREIGN KEY(user_id) REFERENCES users(user_id)
            );
            """)

            # Chat History Table
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS chat_memory (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT,
                role TEXT CHECK(role IN ('user', 'assistant')) NOT NULL,
                content TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(user_id) REFERENCES users(user_id)
            );
            """)

            print("✅ Database schema created successfully.")
    except Exception as e:
        print("❌ Failed to create schema:", e)

if __name__ == "__main__":
    create_advanced_schema()


