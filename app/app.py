from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# ---------- DATABASE INIT ----------
def init_db():
    conn = sqlite3.connect('feedback.db')
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
    conn = sqlite3.connect('feedback.db')

    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        branch = request.form['branch']
        year = request.form['year']
        message = request.form['message']

        conn.execute('''
            INSERT INTO feedback (name, email, phone, branch, year, message)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (name, email, phone, branch, year, message))

        conn.commit()
        return redirect('/')   # prevent duplicate submission

    data = conn.execute("SELECT * FROM feedback").fetchall()
    conn.close()

    return render_template('index.html', data=data)

# ---------- RUN APP -----
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)