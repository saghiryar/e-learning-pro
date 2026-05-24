from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

# Connect database (Video Style)
conn = sqlite3.connect('simple.db', check_same_thread=False)
cursor = conn.cursor()

# Create tables
cursor.execute("CREATE TABLE IF NOT EXISTS users (name TEXT, password TEXT)")
cursor.execute("CREATE TABLE IF NOT EXISTS courses (title TEXT)")
cursor.execute("CREATE TABLE IF NOT EXISTS progress (name TEXT, score INTEGER)")
conn.commit()

current_user = None

@app.route('/')
def home():
    return render_template('index.html')

# --- Register ---
@app.route('/register', methods=['POST'])
def register():
    name = request.form.get('username')
    password = request.form.get('password')
    cursor.execute("INSERT INTO users VALUES (?, ?)", (name, password))
    conn.commit()
    return "Registered successfully! <a href='/'>Go Back</a>"

# --- Login ---
@app.route('/login', methods=['POST'])
def login():
    global current_user
    name = request.form.get('username')
    password = request.form.get('password')
    cursor.execute("SELECT * FROM users WHERE name=? AND password=?", (name, password))
    user = cursor.fetchone()
    
    if user:
        current_user = name
        return f"Login successful! Welcome {name}. <a href='/'>Go Back</a>"
    else:
        return "Wrong details! <a href='/'>Go Back</a>"

# --- Add Course ---
@app.route('/add_course', methods=['POST'])
def add_course():
    title = request.form.get('course')
    cursor.execute("INSERT INTO courses VALUES (?)", (title,))
    conn.commit()
    return "Course added! <a href='/'>Go Back</a>"

# --- Quiz ---
@app.route('/quiz', methods=['POST'])
def quiz():
    ans = request.form.get('q1')
    if ans == "yes":
        return "Correct Answer! <a href='/'>Go Back</a>"
    else:
        return "Wrong! <a href='/'>Go Back</a>"

if __name__ == "__main__":
    app.run(debug=True)