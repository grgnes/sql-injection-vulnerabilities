from flask import Flask, request, render_template_string
import sqlite3

app = Flask(__name__)

# Start and create the database with example users
def init_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    # Clear existing data
    c.execute("DELETE FROM users")

    # Add example users
    c.execute("INSERT INTO users (username, password) VALUES (?, ?)",
              ('admin', 'admin123'))
    c.execute("INSERT INTO users (username, password) VALUES (?, ?)",
              ('user1', 'password1'))
    c.execute("INSERT INTO users (username, password) VALUES (?, ?)",
              ('user2', 'password2'))

    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template_string('''
        <form method="POST" action="/login">
            <input type="text" name="username" placeholder="Kullanıcı adı" required>
            <input type="password" name="password" placeholder="Şifre" required>
            <button type="submit">Giriş Yap</button>
        </form>
    ''')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    conn = sqlite3.connect('users.db')
    c = conn.cursor()

    # Vulnerable SQL query
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    print("[DEBUG] Working query:", query)

    c.execute(query)
    user = c.fetchone()
    conn.close()

    if user:
        return f"Wellcome, {user[1]}!"
    else:
        return "Invalid login. Please try again."

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
