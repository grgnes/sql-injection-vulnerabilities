from flask import Flask, request, render_template_string
import sqlite3
import os

app = Flask(__name__)

DB_FILE = "shop.db"

# Create the database and tables if they don't exist
def init_db():
    # Clean up any existing database
    if not os.path.exists(DB_FILE):
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()

        # Analytics table for tracking visitors
        c.execute("CREATE TABLE analytics (id INTEGER PRIMARY KEY, tracking_id TEXT);")
        c.execute("INSERT INTO analytics (tracking_id) VALUES ('abc123');")

        # Users table for authentication
        c.execute("CREATE TABLE users (username TEXT, password TEXT);")
        c.execute("INSERT INTO users VALUES ('administrator', 'secretpass');")

        conn.commit()
        conn.close()

def get_db():
    return sqlite3.connect(DB_FILE)

@app.route('/')
def index():
    tracking = request.cookies.get('TrackingId', '')

    # Vulnerable SQL query
    query = "SELECT id FROM analytics WHERE tracking_id = '" + tracking + "';"
    conn = get_db()
    cur = conn.cursor()

    try:
        cur.execute(query)   
        rows = cur.fetchall()
    except Exception as e:
        conn.close()
        return f"<h1>SQL Error: {e}</h1>"

    conn.close()

    if len(rows) > 0:
        msg = "Welcome back"
    else:
        msg = "Hello visitor"

    return render_template_string("<h1>{{msg}}</h1>", msg=msg)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
