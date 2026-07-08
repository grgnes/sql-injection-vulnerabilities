from flask import Flask, request
import sqlite3

app = Flask(__name__)

# Start and create the database with example items
def init_db():
    conn = sqlite3.connect('products.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            released INTEGER NOT NULL
        )
    ''')
    # Clear existing data
    c.execute("DELETE FROM products")

    # Add example items (released=0 means not released yet)
    c.execute("INSERT INTO products (name, category, released) VALUES (?, ?, ?)",
              ('iPhone', 'electronics', 1))
    c.execute("INSERT INTO products (name, category, released) VALUES (?, ?, ?)",
              ('Prototype Phone', 'electronics', 0))
    c.execute("INSERT INTO products (name, category, released) VALUES (?, ?, ?)",
              ('T-Shirt', 'clothing', 1))
    c.execute("INSERT INTO products (name, category, released) VALUES (?, ?, ?)",
              ('Secret Jacket', 'clothing', 0))

    conn.commit()
    conn.close()

@app.route('/search')
def search():
    category = request.args.get('category', '')

    conn = sqlite3.connect('products.db')
    c = conn.cursor()

    # Vulnerable SQL query
    query = f"SELECT name FROM products WHERE category = '{category}' AND released = 0"
    print("[DEBUG] Çalışan sorgu:", query)

    c.execute(query)
    results = c.fetchall()
    conn.close()

    if results:
        return '<br>'.join([r[0] for r in results])
    else:
        return "NO RESULTS"

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
