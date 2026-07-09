from flask import Flask, request, render_template_string
import sqlite3
import os

app = Flask(__name__)

def init_db():
    # Clean up any existing database
    if os.path.exists("lab.db"):
        os.remove("lab.db")

    conn = sqlite3.connect("lab.db")
    cur = conn.cursor()
    # Create a orginal products table with 3 columns (id, name, price)
    cur.execute("CREATE TABLE products (id INTEGER PRIMARY KEY, name TEXT, price REAL)")
    cur.executemany("INSERT INTO products (id, name, price) VALUES (?, ?, ?)", [
        (1, "Hammer", 10.5),
        (2, "Screwdriver", 7.25),
        (3, "Drill", 25.0),
    ])

    # Create a secret users table with 3 columns (id, username, password)
    cur.execute("CREATE TABLE users_secret (id INTEGER PRIMARY KEY, username TEXT, password TEXT)")
    cur.executemany("INSERT INTO users_secret (id, username, password) VALUES (?, ?, ?)", [
        (1, "admin", "admin123"),
        (2, "moren", "123moren"),
    ])

    conn.commit()
    conn.close()

@app.route("/products")
def products():
    # Get the category parameter from the query string
    category = request.args.get("category", "")
    conn = sqlite3.connect("lab.db")
    cur = conn.cursor()

    # Vulnerable SQL query
    query = f"SELECT id, name, price FROM products WHERE name LIKE '%{category}%'"
    try:
        rows = cur.execute(query).fetchall()
    except Exception as e:
        rows = [(f"SQL error: {e}", "", "")]

    conn.close()

    # Render the results in a simple HTML format
    html = "<h1>Products (only name shown)</h1><ul>"
    for r in rows:
        # r[1] => name
        html += f"<li>{r[1]}</li>"
    html += "</ul>"
    return render_template_string(html)

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
