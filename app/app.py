from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('feedback.db')
    conn.execute('CREATE TABLE IF NOT EXISTS feedback (name TEXT, message TEXT)')
    conn.close()

@app.route('/', methods=['GET', 'POST'])
def index():
    conn = sqlite3.connect('feedback.db')
    if request.method == 'POST':
        name = request.form['name']
        message = request.form['message']
        conn.execute("INSERT INTO feedback VALUES (?, ?)", (name, message))
        conn.commit()

    data = conn.execute("SELECT * FROM feedback").fetchall()
    conn.close()
    return render_template('index.html', data=data)

if __name__ == "__main__":
    init_db()
    app.run(host='0.0.0.0', port=5000)