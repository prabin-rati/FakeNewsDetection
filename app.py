import os
import sqlite3
import joblib
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'bca_project_2026_prabin'

# --- DATABASE SETUP ---
def get_db():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(base_dir, 'users.db')
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

# --- LOAD ML MODELS (With Safety Check) ---
model = None
vectorizer = None
try:
    model_path = 'fake_news_model.sav'
    vect_path = 'vectorizer.sav'
    if os.path.exists(model_path) and os.path.exists(vect_path):
        model = joblib.load(model_path)
        vectorizer = joblib.load(vect_path)
        print("✅ ML Model loaded successfully!")
    else:
        print("⚠️ Warning: .sav files missing. Predictions will be simulated.")
except Exception as e:
    print(f"ML Loading Error: {e}")

# --- ROUTES ---

@app.route('/')
def home():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('index.html', username=session.get('username'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        fname = request.form.get('first_name')
        lname = request.form.get('last_name')
        uname = request.form.get('username')
        email = request.form.get('email')
        pwd_raw = request.form.get('password')

        if not all([fname, lname, uname, email, pwd_raw]):
            flash("All fields are required!")
            return render_template('signup.html')

        hashed_pwd = generate_password_hash(pwd_raw)
        db = get_db()
        try:
            db.execute('''INSERT INTO users (first_name, last_name, username, email, password, role) 
                          VALUES (?, ?, ?, ?, ?, ?)''',
                       (fname, lname, uname, email, hashed_pwd, 'user'))
            db.commit()
            flash("Registration successful! Please login.")
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash("Username or Email already exists!")
        finally:
            db.close()
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        uname_raw = request.form.get('username')
        pwd_raw = request.form.get('password')

        if not uname_raw or not pwd_raw:
            flash("Please enter credentials.")
            return render_template('login.html')

        uname = uname_raw.strip()
        pwd = pwd_raw.strip()

        db = get_db()
        user = db.execute('SELECT * FROM users WHERE username = ?', (uname,)).fetchone()
        db.close()

        if user and check_password_hash(user['password'], pwd):
            session.clear()
            session['user_id'] = user['id']
            session['username'] = user['username']
            return redirect(url_for('home'))
        else:
            flash("Invalid Username or Password!")
            
    return render_template('login.html')

@app.route('/predict', methods=['POST'])
def predict():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    news_text = request.form.get('news_text')
    if not news_text:
        return redirect(url_for('home'))

    # If model is loaded, use it. Otherwise, use a placeholder.
    if model and vectorizer:
        vec_text = vectorizer.transform([news_text])
        pred = model.predict(vec_text)
        result = "FAKE" if pred[0] == 0 else "REAL"
    else:
        result = "REAL (Simulation - Model Files Missing)"

    # Save to History
    db = get_db()
    db.execute('INSERT INTO history (user_id, news_text, result, timestamp) VALUES (?, ?, ?, ?)',
               (session['user_id'], news_text[:100], result, datetime.now().strftime("%Y-%m-%d %H:%M")))
    db.commit()
    db.close()

    return render_template('index.html', result=result, original_text=news_text, username=session['username'])

# --- THE MISSING ROUTE THAT CAUSED YOUR ERROR ---
 # 1. This route SHOWS the history page (The one causing the error)
@app.route('/history')
def history():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    db = get_db()
    # Fetching history to display in the table
    user_history = db.execute('SELECT * FROM history WHERE user_id = ? ORDER BY id DESC', 
                              (session['user_id'],)).fetchall()
    db.close()
    return render_template('history.html', history=user_history)

# 2. This route DELETES the history
@app.route('/clear_history', methods=['POST'])
def clear_history():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    db = get_db()
    db.execute('DELETE FROM history WHERE user_id = ?', (session['user_id'],))
    db.commit()
    db.close()
    
    flash("History cleared successfully!")
    return redirect(url_for('history')) # Redirects back to the SHOW route above

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)