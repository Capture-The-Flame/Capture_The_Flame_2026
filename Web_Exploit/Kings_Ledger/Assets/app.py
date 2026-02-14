from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
import hashlib

app = Flask(__name__)
app.secret_key = 'ctf_secret_key_change_this'

DATABASE = 'users.db'

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            is_admin INTEGER DEFAULT 0
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS activity_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            action TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS secrets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            secret_name TEXT NOT NULL,
            secret_value TEXT NOT NULL
        )
    ''')
    
    # Insert admin user
    admin_password = hashlib.md5('admin123'.encode()).hexdigest()
    cursor.execute('INSERT OR IGNORE INTO users (username, password, is_admin) VALUES (?, ?, ?)',
                   ('admin', admin_password, 1))
    
    # Insert the flag
    cursor.execute('INSERT OR IGNORE INTO secrets (secret_name, secret_value) VALUES (?, ?)',
                   ('flag', 'flames{SqL_1nj3ct10n_m4st3r}'))
    
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        hashed_password = hashlib.md5(password.encode()).hexdigest()
        
        conn = get_db()
        cursor = conn.cursor()
        
        try:
            # SAFE: Using parameterized query
            cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)',
                         (username, hashed_password))
            conn.commit()
            
            # Log registration
            cursor.execute('INSERT INTO activity_logs (username, action) VALUES (?, ?)',
                         (username, 'User registered'))
            conn.commit()
            
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('Username already exists!', 'error')
        finally:
            conn.close()
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        hashed_password = hashlib.md5(password.encode()).hexdigest()
        
        conn = get_db()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?',
                      (username, hashed_password))
        user = cursor.fetchone()
        conn.close()
        
        if user:
            session['username'] = user['username']
            session['is_admin'] = user['is_admin']
            
            flash('Login successful!', 'success')
            if user['is_admin']:
                return redirect(url_for('admin'))
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials!', 'error')
    
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    return render_template('dashboard.html', username=session['username'])

@app.route('/admin')
def admin():
    if 'username' not in session or not session.get('is_admin'):
        flash('Access denied! Admin only.', 'error')
        return redirect(url_for('login'))
    
    conn = get_db()
    cursor = conn.cursor()
    
    # Get all usernames from users table
    cursor.execute('SELECT username FROM users WHERE is_admin = 0')
    usernames = cursor.fetchall()
    
    user_activities = []
    
    # Executing username directly as SQL query
    for user_row in usernames:
        username = user_row['username']
        
        try:
            # This executes the username as a SQL query
            cursor.execute(username)
            results = cursor.fetchall()
            
            # Format results to display
            activities = []
            for row in results:
                # Convert row to dict-like format for template
                row_dict = {}
                for idx, col in enumerate(cursor.description):
                    row_dict[col[0]] = row[idx]
                activities.append(row_dict)
            
            user_activities.append({
                'username': username,
                'activities': activities
            })
        except sqlite3.Error as e:
            # If query fails, show error
            user_activities.append({
                'username': username,
                'activities': [{'error': f'Query Error: {str(e)}'}]
            })
    
    conn.close()
    
    return render_template('admin.html', user_activities=user_activities)

@app.route('/schema')
def schema():
    """Debug endpoint - TODO: Remove before production!"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT name, sql FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    conn.close()
    
    schema_info = "<h1>Database Schema (Debug)</h1>"
    schema_info += "<p style='color: red;'>WARNING: This endpoint should be removed in production!</p>"
    for table in tables:
        schema_info += f"<h3>Table: {table['name']}</h3>"
        schema_info += f"<pre>{table['sql']}</pre><br>"
    
    return schema_info

@app.route('/clean')
def clean():
    conn=get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE username LIKE '%SELECT%' OR password LIKE '%SELECT%';")
    conn.commit()
    cursor.execute("DELETE FROM activity_logs WHERE username LIKE '%SELECT%';")
    conn.commit()
    cursor.execute("DELETE FROM activity_logs WHERE username LIKE 'ed';")
    conn.commit()
    cursor.execute("DELETE FROM activity_logs WHERE username LIKE '.tables';")
    conn.commit()
    cursor.execute("DELETE FROM users WHERE username LIKE 'ed' OR password LIKE '%SELECT%';")
    conn.commit()
    cursor.execute("DELETE FROM users WHERE username LIKE '.tables' OR password LIKE '%SELECT%';")
    conn.commit()
    # conn.close()
    return "Deleted all entries containing SELECT"

@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully!', 'success')
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)