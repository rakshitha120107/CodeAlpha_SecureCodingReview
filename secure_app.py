import sqlite3
import os
import subprocess
import json
from markupsafe import escape
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, request, redirect, abort

app = Flask(__name__)

# Fix 1: Load secret key from environment
app.secret_key = os.environ.get("FLASK_SECRET_KEY")

DB_PATH = "users.db"
ALLOWED_PING_TARGETS = {"localhost", "127.0.0.1"}

def get_db():
    conn = sqlite3.connect(DB_PATH)
    return conn

def init_db():
    conn = get_db()
    conn.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, password_hash TEXT)")
    # Fix 2: Store hashed password
    conn.execute("INSERT OR IGNORE INTO users (id, username, password_hash) VALUES (1, 'admin', ?)",
        (generate_password_hash("admin123"),))
    conn.commit()
    conn.close()

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")
        conn = get_db()
        # Fix 3: Parameterized query
        cursor = conn.execute("SELECT id, username, password_hash FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()
        conn.close()
        if user and check_password_hash(user[2], password):
            return redirect("/welcome")
        return "Invalid credentials", 401
    return """
        <form method="post">
            Username: <input name="username"><br>
            Password: <input name="password" type="password"><br>
            <input type="submit">
        </form>
    """

@app.route("/welcome")
def welcome():
    user = request.args.get("user", "guest")
    # Fix 4: Escape user input
    safe_user = escape(user)
    return f"<h1>Welcome, {safe_user}!</h1>"

@app.route("/run", methods=["POST"])
def run_command():
    target = request.form.get("host", "")
    # Fix 5: Allow-list + no shell
    if target not in ALLOWED_PING_TARGETS:
        abort(400, "Host not permitted")
    result = subprocess.run(["ping", "-c", "1", target],
        capture_output=True, text=True, timeout=5)
    return f"<pre>{escape(result.stdout)}</pre>"

@app.route("/load", methods=["POST"])
def load_data():
    # Fix 6: Use JSON instead of pickle
    try:
        obj = json.loads(request.data)
    except (ValueError, TypeError):
        abort(400, "Invalid JSON")
    return str(obj)

if __name__ == "__main__":
    init_db()
    # Fix 7: Debug off, local only
    debug_mode = os.environ.get("FLASK_DEBUG", "false").lower() == "true"
    app.run(debug=debug_mode, host="127.0.0.1")
