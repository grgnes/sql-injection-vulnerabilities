from flask import Flask, request
import sqlite3
import os

app = Flask(__name__)

def init_db():
    if os.path.exists("lab.db"):
        os.remove("lab.db")
    conn = sqlite3.connect("lab.db")
    cur = conn.cursor()

    # Create a sample table and insert some data
    cur.execute("CREATE TABLE products (id INTEGER PRIMARY KEY, name TEXT, category TEXT)")
    cur.executemany("INSERT INTO products (id, name, category) VALUES (?, ?, ?)", [
        (1, 'Hammer', 'tools'),
        (2, 'Screwdriver', 'tools'),
        (3, 'Drill', 'tools'),
    ])

    conn.commit()
    conn.close()

@app.route('/products')
def products():
    category = request.args.get('category', '')
    conn = sqlite3.connect("lab.db")
    cur = conn.cursor()

    # Vulnerable SQL query
    query = f"SELECT id, name, category FROM products WHERE category = '{category}'"
    try:
        rows = cur.execute(query).fetchall()
    except Exception as e:
        rows = [(f"SQL error: {e}", '', '')]
    conn.close()
    return '<br>'.join(str(r) for r in rows)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
