from flask import Flask, render_template, request, redirect, url_for, session, flash
import os
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

# Initialize Flask app
app = Flask(__name__, template_folder="../frontend/templates", static_folder='../frontend/static')

# Set the secret key for session management
app.secret_key = os.urandom(24)  # Randomly generated secret key for development

# Path to the SQLite database for user data
DATABASE_PATH = r"F:\c++ Projects\123\website-test\backend\database\user_data\user_data.db"

# Ensure the directory exists
os.makedirs(os.path.dirname(DATABASE_PATH), exist_ok=True)

# Initialize database connection and create necessary tables
def init_db():
    """Initializes the database and creates necessary tables if they do not exist."""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    # Create the 'users' table if it doesn't exist
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        email TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL
    )
    ''')

    conn.commit()  # Commit changes
    conn.close()   # Close the connection

# Call the init_db function to initialize the database (if not already initialized)
init_db()

# Helper function to connect to the SQLite database
def get_db_connection():
    """Returns a connection object to interact with the database."""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row  # To access columns by name (not by index)
    return conn

# Route for the homepage
@app.route("/")
def home():
    """Render the homepage."""
    return render_template("index.html")

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
            with sqlite3.connect(DATABASE_PATH) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
                    (username, email, password_hash),
                )
                conn.commit()
            return redirect(url_for("home"))  # Redirect to home after successful signup
        except sqlite3.IntegrityError:
            return render_template("signup.html", error="Username or email already exists.")

    return render_template("signup.html")

# Route for user login
@app.route('/login', methods=['GET', 'POST'])
def login():
    """Handle the login process."""
    if request.method == 'POST':
        # Make sure these fields exist in the form
        username_or_email = request.form.get('username_or_email')
        password = request.form.get('password')


        # Check if all required fields are present
        if not username_or_email or not password:
            flash("All fields are required.", "error")
            return redirect(url_for('login'))

        # Connect to the database and verify user credentials
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username = ? AND email = ?', (username_or_email))
        user = cursor.fetchone()  # Fetch user if exists

        if user and check_password_hash(user['password'], password):
            # If the user exists and password matches
            session['user_id'] = user['id']  # Store the user's ID in the session
            session['username'] = user['username']  # Store the username in the session
            return redirect(url_for('dashboard'))  # Redirect to dashboard after successful login
        else:
            # If login fails, show an error message
            flash('Invalid username, email or password', 'error')
            return redirect(url_for('login'))  # Stay on the login page

    return render_template('login.html')


# Route for the dashboard (after successful login)
@app.route('/dashboard')
def dashboard():
    """Render the dashboard page for the logged-in user."""
    if 'user_id' not in session:
        # If the user is not logged in, redirect to login
        return redirect(url_for('login'))
    
    # Check if the logged-in user is an admin
    if session['username'] == 'admin':
        return redirect(url_for('create_post'))  # Redirect admin to create wellbeing posts
    return render_template('dashboard.html')

# Admin route to create wellbeing posts
@app.route("/admin/create_post", methods=["GET", "POST"])
def create_post():
    """Allow the admin to create wellbeing content."""
    if 'user_id' not in session or session['username'] != 'admin':
        # If the user is not logged in as admin, redirect to the home page
        return redirect(url_for('home'))
    
    if request.method == "POST":
        title = request.form['title']
        description = request.form['description']
        media_type = request.form['media_type']  # 'image', 'video', or 'text'
        media_url = request.form['media_url']   # URL for image/video

        # Save the post to the database
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO wellbeing_content (title, description, media_type, media_url)
            VALUES (?, ?, ?, ?)
        """, (title, description, media_type, media_url))
        conn.commit()
        conn.close()

        flash("Post created successfully", "success")
        return redirect(url_for('wellbeing'))  # Redirect to wellbeing content page

    return render_template("create_post.html")

if __name__ == "__main__":
    app.run(debug=True)
