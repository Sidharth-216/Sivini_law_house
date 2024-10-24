# app.py
from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import secrets
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os  # For environment variables
from database import connect_to_database
import time
from flask_mail import Mail,Message
import datetime
from flask_ngrok import run_with_ngrok

app = Flask(__name__)
#run_with_ngrok(app)
@app.route('/')
def home():
    return render_template('index.html') 

@app.route('/index')
def index():
    return render_template('index.html')

# Email sending function using SMTP
def send_email(to_email, subject, body):
    from_email = os.environ.get('sidupatnaik216@gmail.com')  # Your email address
    password = os.environ.get('lnxuhhlinbyrgnvw ')  # Your email password

    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()  # Upgrade the connection to a secure encrypted SSL/TLS connection
            server.login(from_email, password)  # Log in to your email account
            server.send_message(msg)  # Send the email
            print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")

# Test email function
def send_test_email():
    from_email = os.environ.get('sidupatnaik216@gmail.com')
    password = os.environ.get('lnxuhhlinbyrgnvw ')
    to_email = 'sidupatnaik216@gmail.com'  # Replace with your email

    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = 'Test Email'

    body = 'This is a test email from Flask application.'
    msg.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(from_email, password)
            server.send_message(msg)
            print("Test email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")

# Call the test email function (you can comment this out after testing)
send_test_email()

# Configure Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('sidupatnaik216@gmail.com')  # Your email address
app.config['MAIL_PASSWORD'] = os.environ.get('lnxuhhlinbyrgnvw')  # Your email password
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('rohitptnk216@gmail.com')  # Default sender

mail = Mail(app)  # Initialize the Mail object

app.secret_key = secrets.token_hex(16)  # Generates a random 32-character hex string
print("Secret key set:", app.secret_key)  # Debugging output

# app.py
# ... existing imports ...

def initialize_contact_table():
    conn = connect_to_database()
    cursor = conn.cursor()
    try:
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS contact (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                number TEXT NOT NULL,
                subject TEXT NOT NULL,
                message TEXT NOT NULL      
            );
        ''')
        conn.commit()  # Commit the transaction
    except Exception as e:
        print(f"An error occurred while initializing the contact table: {e}")
    finally:
        cursor.close()
        conn.close()

# Call this function when your application starts
initialize_contact_table()

# Email sending function using SMTP
def send_email(to_email, subject, body):
    msg = Message(subject, recipients=[to_email])
    msg.body = body
    try:
        mail.send(msg)
        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")


@app.route('/homepage', methods=['GET', 'POST'])
def homepage():
    if request.method == 'POST':
        # Get form data
        name = request.form['name']
        lawyer_type = request.form['lawyer_type']
        email = request.form['email']
        case_description = request.form['case_description']
        appointment_date = request.form['appointment_date']
        time_of_booking = request.form['time_of_booking']
        date_of_booking = request.form['date_of_booking']
        username = session.get('username')

        # Store booking details in the database
        try:
            execute_with_retry("""
                INSERT INTO bookings 
                (name, lawyer_type, email, case_description, appointment_date, time_of_booking, date_of_booking, username) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (name, lawyer_type, email, case_description, appointment_date, time_of_booking, date_of_booking, username))
            return redirect(url_for('profile'))  # Redirect after successful submission
        except Exception as e:
            return f"An error occurred: {e}"

    # If GET request, render the homepage
    return render_template('homepage.html')


def connect_to_database():
    return sqlite3.connect('lawfirm.db', timeout=30)  # Increased timeout

def execute_with_retry(query, params=(), retries=5):
    for attempt in range(retries):
        try:
            with connect_to_database() as conn:
                conn.execute('PRAGMA journal_mode=WAL;')  # Enable Write-Ahead Logging
                cursor = conn.cursor()
                cursor.execute(query, params)
                conn.commit()
                return cursor
        except sqlite3.OperationalError as e:
            if "database is locked" in str(e) and attempt < retries - 1:
                time.sleep(0.5)  # Wait before retrying
            else:
                raise  # Re-raise the exception if it's not a lock issue or max retries reached

# Example usage
def initialize_database():
    try:
        execute_with_retry('''
            CREATE TABLE IF NOT EXISTS clients (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                name TEXT NOT NULL,
                paswd TEXT NOT NULL,
                cnfpas TEXT NOT NULL,
                gender TEXT,
                email TEXT NOT NULL,
                number TEXT NOT NULL
            );
        ''')

        execute_with_retry('''
            CREATE TABLE IF NOT EXISTS bookings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                lawyer_type TEXT NOT NULL,
                email TEXT NOT NULL,
                case_description TEXT NOT NULL,
                appointment_date TEXT NOT NULL,
                time_of_booking TEXT NOT NULL,
                date_of_booking TEXT NOT NULL,
                username TEXT NOT NULL,
                FOREIGN KEY (username) REFERENCES clients(username)
            );
        ''')
        execute_with_retry('''
            CREATE TABLE IF NOT EXISTS contact (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                number TEXT NOT NULL,
                subject TEXT NOT NULL,
                message TEXT NOT NULL      
            );
        ''')
        
    except Exception as e:
        print(f"An error occurred while initializing the database: {e}")
# Call this function when your application starts
initialize_database()


# ... existing code ...

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        name = request.form.get('name')
        cnfpas = request.form.get('cnfpas')
        paswd = request.form.get('paswd')
        gender = request.form.get('gender')
        email = request.form.get('email')
        number = request.form.get('number')
        
        if paswd != cnfpas:
            return "Passwords do not match."
        
        conn = connect_to_database()
        cursor = conn.cursor()
        try:
            # Create clients table if it doesn't exist
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS clients (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL,
                    name TEXT NOT NULL,
                    paswd TEXT NOT NULL,
                    cnfpas TEXT NOT NULL,
                    gender TEXT,
                    email TEXT NOT NULL,
                    number TEXT NOT NULL
                );
            ''')

            # Insert user data into the database
            query = "INSERT INTO clients (username, name,cnfpas,paswd, gender, email, number) VALUES (?,?,?,?,?,?,?)"

            cursor.execute(query, (username, name,cnfpas, paswd, gender, email, number))  # Added parameters for the query
            conn.commit()  # Commit the transaction

            # Verify if the data is inserted correctly
            cursor.execute("SELECT * FROM clients WHERE username = ?", (username,))
            user = cursor.fetchone()

            if user:
                return redirect(url_for('login'))
            else:
                return "Registration failed. Please try again."
        except Exception as e:
            conn.rollback()  # Rollback in case of an error
            print(f"An error occurred: {e}")  # Log the exact error for debugging
            return f"An error occurred: {e}"
        finally:
            cursor.close()
            conn.close()
        
    return render_template('register.html')

# ... existing code ...
@app.route('/team')
def team():
    return render_template('team.html')

from flask import session  # Import session to manage user sessions

# ... existing code ...

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        paswd = request.form.get('paswd')

        conn = connect_to_database()  # Ensure this connects to the correct database
        cursor = conn.cursor()
        try:
            # Check if the user exists with the provided username and password
            cursor.execute("SELECT * FROM clients WHERE username = ? AND paswd = ?", (username, paswd))
            user = cursor.fetchone()

            if user:
                # Store user information in session
                session['username'] = user[1]  #  username is the first column
                session['email'] = user[6]      #  email is the sixth column
                session['number'] = user[7]  # phone number is the seventh column
                session['profile_picture'] = user[0]  # Assuming profile picture is the zero column
                print("Login successful for user:", username)  # Debugging output
                return redirect(url_for('profile'))  # Redirect to profile after login
            else:
                print("Login failed for user:", username)  # Debugging output
                return redirect(url_for('register'))
        except Exception as e:
            print(f"An error occurred during login: {e}")  # Log the exact error for debugging
            return f"An error occurred during login: {e}"  # Return the error message
        finally:
            cursor.close()
            conn.close()

    return render_template('login.html')

# Add the profile route here

@app.route('/profile')
def profile():
    # Retrieve data from the session
    username = session.get('username')
    email = session.get('email')
    number = session.get('number')

    # Retrieve booking details from the database
    bookings = []  # Initialize an empty list for bookings
    if username:  # Ensure the user is logged in
        conn = connect_to_database()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM bookings WHERE username = ?", (username,))
            bookings = cursor.fetchall()  # Fetch all bookings for the user
        except Exception as e:
            print(f"An error occurred while fetching bookings: {e}")
        finally:
            cursor.close()
            conn.close()

    return render_template('profile.html', username=username, email=email, number=number, bookings=bookings)
# ... existing code ...


@app.route('/about')
def about():
    return render_template('about.html') 




def connect_to_database():
    try:
        conn = sqlite3.connect('lawfirm.db', timeout=30)  # Ensure the path is correct
        print("Database connection established.")
        return conn
    except Exception as e:
        print(f"Failed to connect to database: {e}")
        return None

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        number = request.form.get('number')
        subject = request.form.get('subject')
        message = request.form.get('message')
        

        # Debugging: Print the received form data
        print(f"Received data: Name: {name}, Email: {email}, Number: {number}, Subject: {subject}, Message: {message}")

        try:
            execute_with_retry("""
                INSERT INTO contact 
                (name,  email, number,subject,message) 
                VALUES (?, ?, ?, ?, ?)
            """, (name, email, number,subject,message))
            return redirect(url_for('index'))  # Redirect after successful submission
        except Exception as e:
            return f"An error occurred: {e}"
    return render_template('contact.html')
 # Example usage
def initialize_database():
    try:
        execute_with_retry('''
            CREATE TABLE IF NOT EXISTS contact (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                number TEXT NOT NULL,
                subject TEXT NOT NULL,
                message TEXT  NOT NULL   
            );
        ''')
        
    except Exception as e:
        print(f"An error occurred while initializing the database: {e}")
initialize_database()     
@app.route('/forget')
def forget():
    return render_template('forget.html')


@app.route('/sid')
def sid():
    return render_template('sid.html')

@app.route('/bns')
def bns():
    return render_template('bns.html')

if __name__ == '__main__': # Initialize the database when the app starts
    app.run(debug=True,port=5001)
    #app.run()