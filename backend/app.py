from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
import os
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from chatbot import BushraChatbot
from flask import render_template



# Initialize Flask app
app = Flask(__name__, template_folder="../frontend/templates", static_folder='../frontend/static')

# Set the secret key for session management
app.secret_key = os.urandom(24)



# Paths to the SQLite databases
MAIN_DATABASE_PATH = os.path.join(os.path.dirname(__file__), 'database/mental_wellness.db')
CHATBOT_DB_PATH = os.path.join(os.path.dirname(__file__), 'database/chatbot_data/chatbot_data.db')
EMOTIONS_DB_PATH = os.path.join(os.path.dirname(__file__), 'database/emotions_data/emotions_data.db')
POSTS_PATH = os.path.join(os.path.dirname(__file__), 'database/chatbot_data/posts.db')
POSTS_DIR_PATH = os.path.join(os.path.dirname(__file__), 'database/chatbot_data')  # Directory path

# Ensure the directories exist and do not try to create files

def ensure_directories():
    try:
        if not os.path.exists(os.path.dirname(MAIN_DATABASE_PATH)):
            os.makedirs(os.path.dirname(MAIN_DATABASE_PATH), exist_ok=True)
        
        if not os.path.exists(os.path.dirname(CHATBOT_DB_PATH)):
            os.makedirs(os.path.dirname(CHATBOT_DB_PATH), exist_ok=True)
        
        if not os.path.exists(os.path.dirname(EMOTIONS_DB_PATH)):
            os.makedirs(os.path.dirname(EMOTIONS_DB_PATH), exist_ok=True)

        if not os.path.exists(POSTS_PATH):
            os.makedirs(POSTS_DIR_PATH, exist_ok=True)  # Corrected this line
    except Exception as e:
        print(f"Error creating directories: {e}")
        raise

def init_databases():
    try:
        # Main database
        with sqlite3.connect(MAIN_DATABASE_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                email TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL
            )
            ''')
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS wellbeing_content (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                media_type TEXT,
                media_url TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            ''')
            cursor.execute('''
            INSERT OR IGNORE INTO users (username, email, password)
            VALUES (?, ?, ?)
            ''', ("admin", "admin@mentalwellness.com", generate_password_hash("admin123")))
            conn.commit()

        # Chatbot database
        with sqlite3.connect(CHATBOT_DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS chat_conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                message TEXT NOT NULL,
                sender TEXT NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            ''')
            conn.commit()

        # Emotions database
        with sqlite3.connect(EMOTIONS_DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS detected_emotions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                emotion TEXT NOT NULL,
                confidence REAL NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            ''')
            conn.commit()

        # Initialize posts database
        if not os.path.exists(POSTS_PATH):  # This checks if the posts.db file exists
            with sqlite3.connect(POSTS_PATH) as conn:
                cursor = conn.cursor()
                cursor.execute('''CREATE TABLE posts (
                                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                                    title TEXT NOT NULL,
                                    content TEXT NOT NULL,
                                    image_url TEXT,
                                    video_url TEXT,
                                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                                )''')
                conn.commit()
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
        raise

# Ensure directories and initialize databases
ensure_directories()
init_databases()
# Helper function to connect to a SQLite database
def get_db_connection(db_path):
    """Returns a connection object to interact with the specified database."""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row  # To access columns by name
    return conn




# Route for the homepage
@app.route('/')
def index():
    logged_in = 'user_id' in session
    return render_template('index.html', loggedIn=logged_in)


# Route for user signup
@app.route("/signup", methods=["GET", "POST"])
def signup():
    """Handle the signup process."""
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")

        # Hash the password for security
        password_hash = generate_password_hash(password)

        # Save the user in the database
        try:
            with get_db_connection(MAIN_DATABASE_PATH) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
                    (username, email, password_hash),
                )
                conn.commit()
            flash("Signup successful! Please log in.", "success")
            return redirect(url_for("login"))
        except sqlite3.IntegrityError:
            flash("Username or email already exists.", "error")
            return redirect(url_for("signup"))

    return render_template("signup.html")

# Route for user login
@app.route('/login', methods=['GET', 'POST'])
def login():
    """Handle the login process."""
    if request.method == 'POST':
        username_or_email = request.form.get('username_or_email')
        password = request.form.get('password')

        conn = get_db_connection(MAIN_DATABASE_PATH)
        cursor = conn.cursor()
        cursor.execute(
            'SELECT * FROM users WHERE username = ? OR email = ?', 
            (username_or_email, username_or_email)
        )
        user = cursor.fetchone()
        conn.close()

        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            flash("Login successful!", "success")
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username, email, or password.', 'error')
            return redirect(url_for('login'))

    return render_template('login.html')

# Route for user logout
@app.route("/logout")
def logout():
    """Logs out the user by clearing the session."""
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for("login"))

# Route for the dashboard
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('index.html', loggedIn=True)


# Route for chatbot
# Initialize the chatbot
bushra = BushraChatbot()

@app.route('/chatbot', methods=['GET', 'POST'])
def chatbot():
    """Chatbot interface for user interaction."""
    # Check if the user is logged in
    if 'user_id' not in session:
        flash("Please log in to use the chatbot.", "error")
        return redirect(url_for('login'))
    
    user_id = session['user_id']  # Get the logged-in user's ID
    messages = []  # Initialize a list to store chat messages

    if request.method == 'POST':
        try:
            user_message = request.form['message']  # Get the user's message from the form
            
            # Process the message using the chatbot
            chatbot_response_data = bushra.process_message(user_message)
            chatbot_response = chatbot_response_data['response']
            emotion = chatbot_response_data['emotion']
            confidence = chatbot_response_data['confidence']
            
            # Save the user's message and chatbot's response to the chatbot database
            with get_db_connection(CHATBOT_DB_PATH) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO chat_conversations (user_id, message, sender) VALUES (?, ?, ?)",
                    (user_id, user_message, 'user')
                )
                cursor.execute(
                    "INSERT INTO chat_conversations (user_id, message, sender) VALUES (?, ?, ?)",
                    (user_id, chatbot_response, 'chatbot')
                )
                conn.commit()
            
            # Save the detected emotion to the emotions database
            with get_db_connection(EMOTIONS_DB_PATH) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO detected_emotions (user_id, emotion, confidence) VALUES (?, ?, ?)",
                    (user_id, emotion, confidence)
                )
                conn.commit()

            # Provide feedback to the user
            flash(f"Bushra: {chatbot_response}", "chatbot")
        except Exception as e:
            flash(f"An error occurred: {str(e)}", "error")
            return redirect(url_for('chatbot'))

    # Retrieve previous chat messages for the user
    try:
        with get_db_connection(CHATBOT_DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT message, sender, timestamp FROM chat_conversations WHERE user_id = ? ORDER BY timestamp",
                (user_id,)
            )
            messages = cursor.fetchall()
    except Exception as e:
        flash(f"Could not load chat history: {str(e)}", "error")

    return render_template("chatbot.html", messages=messages)





# Route to add a new post (admin only)
@app.route('/write_article', methods=['GET', 'POST'])
def write_article():
    """Allow the admin to write a new article."""
    if 'user_id' not in session:
        flash("You need to log in to write an article.", "warning")
        return redirect(url_for('login'))

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        image_url = request.form['image_url']
        video_url = request.form['video_url']

        # Insert the new post into the database
        conn = get_db_connection(POSTS_PATH)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO posts (title, content, image_url, video_url)
            VALUES (?, ?, ?, ?)
        ''', (title, content, image_url, video_url))
        conn.commit()
        conn.close()

        flash("Article successfully added!", "success")
        return redirect(url_for('wellbeing'))

    return render_template('write_article.html')

# Route to display wellbeing page with articles (view posts)
@app.route('/wellbeing')
def wellbeing():
    """Display all articles in the wellbeing section."""
    conn = get_db_connection(POSTS_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM posts ORDER BY created_at DESC')  # Order by creation date
    posts = cursor.fetchall()
    conn.close()

    return render_template('wellbeing.html', posts=posts)





# Route for Guided Exercise page
@app.route('/exercise')
def exercise():
    return render_template('exercise.html')

# Route for Relaxation Music page
@app.route('/music')
def music():
    return render_template('music.html')

# Route for Guided Meditation page
@app.route('/meditation')
def meditation():
    return render_template('meditation.html')

# Route for Self Journaling page
@app.route('/journaling')
def journaling():
    return render_template('journaling.html')






# Route for the profile page
@app.route('/profile')
def profile():
    """Render the profile page for the logged-in user."""
    if 'user_id' not in session:
        return redirect(url_for('login'))  # Redirect to login if not logged in

    # Here you can query the user's data or just render a simple template
    return render_template('profile.html')  # You need to create this template



if __name__ == "__main__":
    app.run(debug=True)
