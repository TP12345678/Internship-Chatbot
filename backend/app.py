from flask import Flask, request, jsonify
from main_buffer import ask_idc_chatbot
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)  

def get_db():
    conn = sqlite3.connect("users.db")
    conn.row_factory = sqlite3.Row
    return conn

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

@app.route("/")
def home():
    return "IDC Chatbot API is running."

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()

    if not data or "query" not in data:
        return jsonify({"error": "Missing query in request"}), 400

    user_query = data["query"]
    response = ask_idc_chatbot(user_query)

    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True)
