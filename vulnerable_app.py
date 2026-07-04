import sqlite3
import os
import pickle
from flask import Flask, request, render_template_string, redirect

app = Flask(__name__)

# Finding 1: Hardcoded secret key
app.secret_key = "supersecret123"

DB_PATH = "users.db"

def get_db():
    conn = sqlite3.connect(DB_PATH)
    return conn

def init_db():
    conn = get_db()
    conn.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)")
    # Finding 2: Plaintext password storage
    conn.execute("INSERT OR IGNORE INTO users (id, username, password) VALUES (1, 'admin', 'admin123')")
    conn.commit()
    conn.close()

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        conn = get_db()
        # Finding 3: SQL Injection
        query = "SELECT * FROM users WHERE username = '" + username + "' AND password = '" + password + "'"
        cursor = conn.execute(query)
        user = cursor.fetchone()
        conn.close()
        if user:
            return redirect("/welcome?user=" + username)
        else:
            return "Invalid credentials"
    return """
        <form method="post">
            Username: <input name="username"><br>
            Password: <input name="password" type="password"><br>
            <input type="submit">
        </form>
    """

@app.route("/welcome")
def welcome():
    user = request.args.get("user", "")
    # Finding 4: XSS
    template = f"<h1>Welcome, {user}!</h1>"
    return render_template_string(template)

@app.route("/run", methods=["POST"])
def run_command():
    target = request.form["host"]
    # Finding 5: Command Injection
    result = os.popen("ping -c 1 " + target).read()
    return f"<pre>{result}</pre>"

@app.route("/load", methods=["POST"])
def load_data():
    raw = request.data
    # Finding 6: Insecure Deserialization
    obj = pickle.loads(raw)
    return str(obj)

if __name__ == "__main__":
    init_db()
    # Finding 7: Debug mode enabled
    app.run(debug=True, host="0.0.0.0")
