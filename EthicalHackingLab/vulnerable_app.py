from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import os

app = Flask(__name__)
app.secret_key = 'super_secret_key_which_is_actually_not_secret'

# Database Setup
DB_NAME = 'users.db'

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users 
                 (id INTEGER PRIMARY KEY, username TEXT, password TEXT)''')
    # Add a dummy admin user if not exists
    c.execute("SELECT * FROM users WHERE username='admin'")
    if not c.fetchone():
        c.execute("INSERT INTO users (username, password) VALUES ('admin', 'admin123')")
    
    # Add a dummy user with weak password
    c.execute("SELECT * FROM users WHERE username='user'")
    if not c.fetchone():
        c.execute("INSERT INTO users (username, password) VALUES ('user', '123456')")
        
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def index():
    return render_template('index.html', user=session.get('user'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # VULNERABLE CODE: SQL Injection
        # Directly interpolating user input into the query string
        query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
        
        print(f"DEBUG: Executing Query: {query}") # For learning purposes
        
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        try:
            c.execute(query) # Using execute with string formatting is DANGEROUS
            user = c.fetchone()
            conn.close()
            
            if user:
                session['user'] = user[1]
                return redirect(url_for('index'))
            else:
                error = 'Invalid credentials'
        except Exception as e:
            error = f"Database Error: {e}"
            
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('index'))

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('q', '')
    # VULNERABLE CODE: Reflected XSS
    # Returning user input directly to the template without sanitization causes XSS
    # Flask's render_template usually escapes, but we will pass it to a place where we might render it unsafely or simulate it.
    # Actually, to make it vulnerable in Flask with render_template, we have to mark it as safe or use {{ query | safe }} in template.
    return render_template('search.html', query=query)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # VULNERABILITY: Weak Password Policy
        # No length checks, no complexity checks.
        
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute(f"INSERT INTO users (username, password) VALUES ('{username}', '{password}')") # Also SQLi vulnerable here technically, but aiming for logic flaw
        conn.commit()
        conn.close()
        
        return redirect(url_for('login'))
    return render_template('signup.html')

if __name__ == '__main__':
    app.run(debug=True, port=5000)
