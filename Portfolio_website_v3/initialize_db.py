from flask import Flask, request, render_template
import sqlite3

app = Flask(__name__)

conn = sqlite3.connect('registration.db')

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,           
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    email TEXT NOT NULL,
    password1 TEXT NOT NULL,
    course TEXT NOT NULL,
    referrer TEXT NOT NULL,
    experience TEXT NOT NULL
);
""")

conn.commit()
conn.close()

def connect_db():
    return sqlite3.connect('registration.db')

def insert_user(title, first_name, last_name, email, password, course, referrer, experience):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (title, first_name, last_name, email, password, course, referrer, experience) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (title, first_name, last_name, email, password, course, referrer, experience))
    conn.commit()
    conn.close()

def get_user_by_username(username):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()
    return user


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        title = request.form['title']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        password1 = request.form['password1']
        password2 = request.form['password2']
        course = request.form['course']
        referrer = request.form['referrer']
        experience = request.form['experience']
        
        # Server-side password validation
        if password1 != password2:
            return "Passwords do not match!", 400  # 400 Bad Request

        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO users (title, first_name, last_name, email, password1, course, referrer, experience)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (title, first_name, last_name, email, password1, course, referrer, experience))
        conn.commit()
        conn.close()

        return "Registration successful!"

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)