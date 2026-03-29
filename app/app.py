from flask import Flask, render_template, request, redirect
import sqlite3
import os

app = Flask(__name__)

# ---------- DATABASE PATH (IMPORTANT FOR EC2) ----------
DB_PATH = os.path.join(os.path.dirname(__file__), "feedback.db")

# ---------- DATABASE INIT ----------
def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute('''
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            phone TEXT,
            branch TEXT,
            year TEXT,
            message TEXT
        )
    ''')
    conn.close()

# ---------- HOME PAGE ----------
@app.route('/', methods=['GET', 'POST'])
def index():
    conn = sqlite3.connect(DB_PATH)

    if request.method == 'POST':
        try:
            name = request.form.get('name')
            email = request.form.get('email')
            phone = request.form.get('phone')
            branch = request.form.get('branch')
            year = request.form.get('year')
            message = request.form.get('message')

            conn.execute('''
                INSERT INTO feedback (name, email, phone, branch, year, message)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (name, email, phone, branch, year, message))

            conn.commit()
            conn.close()

            return redirect('/')

        except Exception as e:
            print("ERROR:", e)
            conn.close()
            return "Internal Server Error"

    data = conn.execute("SELECT * FROM feedback").fetchall()
    conn.close()

    return render_template('index.html', data=data)

# ---------- RUN APP ----------
if __name__ == "__main__":
    init_db()   # IMPORTANT
    app.run(host="0.0.0.0", port=5000)