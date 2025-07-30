from flask import Flask, request, jsonify
from main import ask_idc_chatbot
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)

def get_db():
    conn = sqlite3.connect("users.db")
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def home():
    return "IDC Chatbot API is running."

@app.route("/register", methods=["POST"])
def register_user():
    data = request.get_json()
    name = data.get("name")
    email = data.get("email")

    if not name or not email:
        return jsonify({"error": "Name and email are required."}), 400

    conn = get_db()
    try:
        conn.execute("INSERT INTO users (name, email) VALUES (?, ?)", (name, email))
        conn.commit()
    except sqlite3.IntegrityError:
        return jsonify({"error": "Email already registered."}), 409
    finally:
        conn.close()

    return jsonify({"message": "User registered successfully."})

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    email = data.get("email")
    query = data.get("query")

    if not email or not query:
        return jsonify({"error": "Email and query are required."}), 400

    conn = get_db()
    user = conn.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
    conn.close()

    if not user:
        return jsonify({"error": "Email not registered."}), 403

    response = ask_idc_chatbot(query)
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True)
