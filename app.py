from flask import send_from_directory
from flask import Flask, render_template, request, redirect, url_for, session,flash,g
import sqlite3
import secrets
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os  # For environment variables
from database import connect_to_database
import time
from flask_mail import Mail,Message
from datetime import datetime
from flask_ngrok import run_with_ngrok
from flask_socketio import SocketIO, emit,join_room
from flask import jsonify,abort
from flask_cors import CORS
from werkzeug.utils import secure_filename
from flask_socketio import join_room, leave_room, send, SocketIO
import random
from string import ascii_uppercase
import jwt
import openai
from openai import OpenAIError
import sqlite3
import cv2
import numpy as np
from email.mime.text import MIMEText
from dotenv import load_dotenv

load_dotenv()  # Loads variables from .env
# Define the function to create the dummy model
def create_dummy_face_model():
    # Generate dummy data for training
    face_data = [np.random.randint(0, 255, (50, 50), dtype=np.uint8) for _ in range(10)]
    labels = list(range(1, 11))  # Dummy labels from 1 to 10

    # Initialize the LBPH face recognizer
    face_recognizer = cv2.face.LBPHFaceRecognizer_create()

    # Train the recognizer with dummy data
    face_recognizer.train(face_data, np.array(labels))

    # Save the trained model to a file
    face_recognizer.save('face_recognizer.yml')
    print("Dummy face recognizer model created and saved as 'face_recognizer.yml'.")



# Call the function to create the dummy model
create_dummy_face_model()
#from flask_login import current_user, login_requir
del_count=0
app = Flask(__name__)
CORS(app)
sec=app.config['SECRET_KEY'] = 'secret!'
app.secret_key = sec
otp_storage = {}

socketio = SocketIO(app)
mail=Mail(app)



# Configure Flask-Mail
app.config['MAIL_SERVER']= 'smtp.gmail.com'
app.config['MAIL_PORT']= 587 #465 #587
app.config['MAIL_USERNAME']= os.getenv('DEL_EMAIL')
app.config['MAIL_PASSWORD']= os.getenv('PASSWORD')
app.config['MAIL_USE_TLS']= True
app.config['MAIL_USE_SSL']= False

print("Email:", app.config['MAIL_USERNAME'])
print("Password:", app.config['MAIL_PASSWORD'])

#run_with_ngrok(app)
@app.route('/')
def index_one():
    db = get_db()
    cursor = db.execute('SELECT name, review, rating FROM reviews ORDER BY id DESC LIMIT 5')  # Limit to latest 5 reviews
    client_reviews = cursor.fetchall()
    return render_template('index.html', reviews=client_reviews)


@app.route('/index')
def index():
    db = get_db()
    cursor = db.execute('SELECT name, review, rating FROM reviews ORDER BY id')  # Limit to latest 5 reviews
    client_reviews = cursor.fetchall()
    return render_template('index.html',reviews=client_reviews)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/android_compatibility')
def android_compatibility():
    return render_template('android_compatibility.html')



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
    from_email = os.getenv('DEL_EMAIL')   # Your email address
    password = os.getenv('PASSWORD')  # Your email password

    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()  # Upgrade the connection to a secure encrypted SSL/TLS connection
            server.login(from_email, password)  # Log in to your email account
            server.sendmail(from_email, to_email, msg.as_string())# Send the email
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

        # Validate that the inputs are not empty
        if not appointment_date or not time_of_booking or not date_of_booking:
            return "All fields are required."
        
        username = session.get('username')
        if not username:
            return "User not logged in."

        # Store booking details in the database
        try:
            execute_with_retry("""
                INSERT INTO bookings 
                (name, lawyer_type, email, case_description, appointment_date, time_of_booking, date_of_booking, username) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (name, lawyer_type, email, case_description, appointment_date, time_of_booking, date_of_booking, username))
            
            conn = sqlite3.connect('lawfirm.db')
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO notifications (user_id, message) 
                VALUES (?, ?)
            ''', (username, 'New booking for lawyer: {} by {} at {}'.format(lawyer_type, name, appointment_date)))
            conn.commit()
            conn.close()
            # Send confirmation email to the user
            subject = "Booking Confirmation"
            body = f"Dear {name},\n\nYour booking for a {lawyer_type} on {appointment_date} has been confirmed.\n\nThank you for choosing our service.\n\nBest regards,\nSivini_law_house"
            try:
                send_email(email, subject, body)
                flash("Email sent successfully!", "success")
            except Exception as e:
                    flash(f"Failed to send email: {e}", "error")
            return redirect(url_for('profile'))  # Redirect after successful submission
        except Exception as e:
            return f"An error occurred: {e}"

    # If GET request, render the homepage
    return render_template('homepage.html')

    # If GET request, render the homepage
    return render_template('homepage.html')


def connect_to_database():
    return sqlite3.connect('lawfirm.db', timeout=200)  # Increased timeout

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
            CREATE TABLE IF NOT EXISTS del_counts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                count INTEGER NOT NULL
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
        execute_with_retry('''
        CREATE TABLE IF NOT EXISTS job (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            number TEXT NOT NULL,
            address TEXT NOT NULL,
            position TEXT NOT NULL,
            resume BLOB,
            about TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        execute_with_retry('''
                CREATE TABLE IF NOT EXISTS lawyers (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    email TEXT NOT NULL,
                    law_firm TEXT NOT NULL,
                    expertise TEXT NOT NULL,
                    password TEXT NOT NULL,
                    exprience TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            ''')
        
    except Exception as e:
        print(f"An error occurred while initializing the database: {e}")
# Call this function when your application starts
initialize_database()

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
            #query = "INSERT INTO clients (username, name,cnfpas,paswd, gender, email, number) VALUES (?,?,?,?,?,?,?)"

            #cursor.execute(query, (username, name,cnfpas, paswd, gender, email, number))  # Added parameters for the query
            #conn.commit()  # Commit the transaction

            cursor.execute('''
        INSERT INTO clients (username,name,cnfpas,paswd,gender,email, number)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (username, name, cnfpas, paswd,gender, email,number ))
            
            conn.commit()
            # Send registration email to user
            subject = "Registration successful"
            body = f"Dear {name},\n\nRegistration successful.\n\nYour credentials:\nName: {name}\nUsername: {username}\nPassword: {cnfpas}\nGender: {gender}\nPhone: {number}\n\nPlease don't share your credentials with anyone.\n\nBest regards,\nSivini_law_house"
            try:
                send_email(email, subject, body)
                flash("Email sent successfully!", "success")
            except Exception as e:
                flash(f"Failed to send email: {e}", "error")
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


@app.route('/team')
def team():
    return render_template('team.html')

from flask import session  # Import session to manage user sessions

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
                session['user_id'] = user[0]  # Assuming the first column is user ID
                session['username'] = user[1]  # Assuming the second column is username
                session['email'] = user[6]    # Assuming the seventh column is email
                session['number'] = user[7]   # Assuming the eighth column is phone number # Assuming the ninth column is profile picture path

                print("Login successful for user:", username)  # Debugging output

                # Redirect to the intended page if it exists, otherwise go to profile
                next_page = session.pop('next', None)  # Remove 'next' after using it
                return redirect(next_page or url_for('profile'))  # Redirect after login
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


@app.route('/face_login', methods=['GET', 'POST'])
def face_login():
    # Create a dummy face recognizer model
    def create_dummy_face_model():
        # Generate dummy data for training
        face_data = [np.random.randint(0, 255, (50, 50), dtype=np.uint8) for _ in range(10)]
        labels = list(range(1, 11))  # Dummy labels from 1 to 10

        # Initialize the LBPH face recognizer
        face_recognizer = cv2.face.LBPHFaceRecognizer_create()

        # Train the recognizer with dummy data
        face_recognizer.train(face_data, np.array(labels))

        # Save the trained model to a file
        face_recognizer.save('face_recognizer.yml')
        print("Dummy face recognizer model created and saved as 'face_recognizer.yml'.")

    # Call the function to create the dummy model
    create_dummy_face_model()
    if request.method == 'POST':
        # Handle face authentication logic

        # Load the pre-trained face recognizer and cascade classifier
        face_recognizer = cv2.face.LBPHFaceRecognizer_create()
        face_recognizer.read('face_recognizer.yml')  # Load the trained model
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

        # Access the webcam
        cap = cv2.VideoCapture(0)
        recognized_user = None

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

            for (x, y, w, h) in faces:
                face = gray[y:y + h, x:x + w]
                label, confidence = face_recognizer.predict(face)

                if confidence < 50:  # Confidence threshold
                    recognized_user = label
                    break

            if recognized_user is not None:
                break

            cv2.imshow('Face Authentication', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

        if recognized_user is not None:
            conn = connect_to_database()
            cursor = conn.cursor()
            try:
                # Fetch user details based on recognized user ID
                cursor.execute("SELECT * FROM clients WHERE id = ?", (recognized_user,))
                user = cursor.fetchone()

                if user:
                    # Store user information in session
                    session['user_id'] = user[0]
                    session['username'] = user[1]
                    session['email'] = user[6]
                    session['number'] = user[7]

                    print("Face authentication successful for user:", user[1])  # Debugging output
                    return redirect(url_for('index'))  # Redirect to profile
                else:
                    return "Face authentication failed. User not found."
            except Exception as e:
                print(f"An error occurred during face authentication: {e}")
                return f"An error occurred during face authentication: {e}"
            finally:
                cursor.close()
                conn.close()
        else:
            return "Face authentication failed. Please try again."

    return render_template('face_login.html')

"""@app.route('/new_login', methods=['GET', 'POST'])
def new_login():
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
                session['user_id'] = user[0]  # Assuming the first column is user ID
                session['username'] = user[1]  # Assuming the second column is username
                session['email'] = user[6]    # Assuming the seventh column is email
                session['number'] = user[7]   # Assuming the eighth column is phone number # Assuming the ninth column is profile picture path

                print("Login successful for user:", username)  # Debugging output

                # Redirect to the intended page if it exists, otherwise go to profile
                next_page = session.pop('next', None)  # Remove 'next' after using it
                return redirect(next_page or url_for('profile'))  # Redirect after login
            else:
                print("Login failed for user:", username)  # Debugging output
                return redirect(url_for('register'))
        except Exception as e:
            print(f"An error occurred during login: {e}")  # Log the exact error for debugging
            return f"An error occurred during login: {e}"  # Return the error message
        finally:
            cursor.close()
            conn.close()

    return render_template('new_login.html')"""


# Add the profile route here

@app.route('/profile')
def profile():
    # Retrieve data from the session
    username = session.get('username')
    email = session.get('email')
    number = session.get('number')

    # Retrieve booking details from the database
    bookings = []  # Initialize an empty list for bookings
    invoices=[]
    if username:  # Ensure the user is logged in
        conn = connect_to_database()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM bookings WHERE username = ?", (username,))
            bookings = cursor.fetchall()  # Fetch all bookings for the user
             # Fetch invoices for the logged-in user
            cursor.execute("SELECT * FROM invoices WHERE client_name = ?", (username,))
            invoices = cursor.fetchall()  # Fetch all invoices for the user
        except Exception as e:
            print(f"An error occurred while fetching bookings: {e}")
        finally:
            cursor.close()
            conn.close()
         
    return render_template('profile.html', username=username, email=email, number=number, bookings=bookings,invoices=invoices)



@app.route('/about')
def about():
    return render_template('about.html') 


def connect_to_database():
    try:
        conn = sqlite3.connect('lawfirm.db', timeout=200)  # Ensure the path is correct
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
                (name, email, number, subject, message) 
                VALUES (?, ?, ?, ?, ?)
            """, (name, email, number, subject, message))
            username = session.get('username')
            if not username:
                return "User not logged in."
            conn = sqlite3.connect('lawfirm.db')
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO notifications (user_id, message) 
                VALUES (?, ?)
            ''', (username, 'New contact form submission from {} (Email: {})'.format(name, email)))
            conn.commit()
            conn.close()
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

def send_otp_email(to_email, otp):
    sender = "sivini.lawhouse@gmail.com"
    password = "oscl pjwa zuxt izug "  # use app password for Gmail
    subject = "Password Reset OTP"
    message = f"Subject: {subject}\n\nYour OTP is: {otp}"

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(sender, password)
    server.sendmail(sender, to_email, message)
    server.quit()



@app.route('/forget', methods=['GET', 'POST'])
def forget_password():
    if request.method == 'POST':
        email = request.form['email']
        conn = sqlite3.connect('lawfirm.db')
        cur = conn.cursor()
        cur.execute("SELECT * FROM clients WHERE email = ?", (email,))
        user = cur.fetchone()
        conn.close()
        
        if user:
            otp = str(random.randint(100000, 999999))
            otp_storage[email] = otp
            send_otp_email(email, otp)
            flash('OTP sent to your email.')
            return redirect(url_for('reset_password', email=email))
        else:
            flash('Email not found')
    
    return render_template('forget.html')



@app.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    email = request.args.get('email')

    if request.method == 'POST':
        user_otp = request.form['otp']
        new_password = request.form['new_password']
        confirm_password=request.form['confirm_password']

        if otp_storage.get(email) == user_otp:
            conn = sqlite3.connect('lawfirm.db')
            cur = conn.cursor()
            cur.execute("UPDATE clients SET paswd = ? ,cnfpas= ? WHERE email = ?", (new_password,confirm_password, email))
            conn.commit()
            conn.close()
            otp_storage.pop(email)
            flash('Password reset successfully.')
            return redirect(url_for('login'))
        else:
            flash('Invalid OTP')
    
    return render_template('reset_password.html', email=email)





# Route for the client video call page
@app.route('/client_video')
def client_video():
    return render_template('client_video.html')  # Client Video Call Page

# Route for the lawyer video call page
@app.route('/lawyer_video')
def lawyer_video():
    return render_template('lawyer_video.html')  # Lawyer Video Call Page

# Event to create a room
@socketio.on('create_room')
def create_room(room_id):
    socketio.enter_room(request.sid, room_id)
    room_participants[room_id] = [request.sid]  # Add the host (client or lawyer) to the room
    socketio.emit('room_created', room_id, room=room_id)
    socketio.emit('new_participant', f"Host has created the room {room_id}", room=room_id)

# Event to join an existing room
@socketio.on('join_room')
def join_room(room_id):
    socketio.enter_room(request.sid, room_id)
    
    # Add the participant to the room's participant list
    if room_id in room_participants:
        room_participants[room_id].append(request.sid)
    else:
        room_participants[room_id] = [request.sid]

    # Notify the host
    socketio.emit('new_participant', f"Participant {request.sid} has joined the room", room=room_id)

    # Notify the participant that they have successfully joined
    socketio.emit('room_joined', room_id, room=room_id)

# Event to handle ICE candidates
@socketio.on('candidate')
def candidate(room_id, candidate):
    socketio.emit('candidate', candidate, room=room_id)

# Event to start offer/answer signaling
@socketio.on('ready_to_offer')
def ready_to_offer(room_id):
    socketio.emit('ready_to_offer', room=room_id)

# Event to end the call
@socketio.on('end_call')
def end_call(room_id):
    socketio.leave_room(request.sid, room_id)
    # Remove the participant from the room's participant list
    if room_id in room_participants and request.sid in room_participants[room_id]:
        room_participants[room_id].remove(request.sid)
    socketio.emit('call_ended', room=room_id)
    socketio.emit('participant_left', request.sid, room=room_id)
    
@app.route('/sid')
def sid():
    return render_template('sid.html')

@app.route('/bns')
def bns():
    return render_template('bns.html')

def get_db_connection():
    conn = sqlite3.connect('lawfirm.db', timeout=140)  # Set timeout to 10 seconds
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/apply', methods=['GET', 'POST'])
def apply():
    if request.method == 'POST':
        # Get form data
        name = request.form.get('name')
        email = request.form.get('email')
        number = request.form.get('number')
        address = request.form.get('address')
        position = request.form.getlist('position')  # Get all selected positions
        resume = request.files['resume']  # Handle file upload
        about = request.form.get('about')

        # You can save the resume file if needed
        # resume.save('path_to_save_resume/' + resume.filename)

        # Connect to the database
        conn = get_db_connection()
        cursor = conn.cursor()

        # Create the "job" table if it doesn't exist
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS job_application (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            number TEXT NOT NULL,
            address TEXT NOT NULL,
            position TEXT NOT NULL,
            resume BLOB,
            about TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')

        # Insert the application into the job_application table
        cursor.execute('''
        INSERT INTO job_application (name, email, number, address, position, resume, about)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (name, email, number, address, ', '.join(position), resume.read(), about))

        # Commit changes and close the connection
        conn.commit()
        conn.close()

        flash('Application submitted successfully!', 'success')
        return redirect(url_for('index'))  # Redirect to the index or success page

    return render_template('apply.html')  # Render the job application form

@app.route('/lawyer_profile', methods=['GET'])
def lawyer_profile():
    # Check if the lawyer_id is in the session
    lawyer_id = session.get('lawyer_id')
    if not lawyer_id:
        flash('Please log in to access your profile.', 'error')
        return redirect(url_for('lawyer_login'))

    connection = sqlite3.connect('lawfirm.db')
    cursor = connection.cursor()
    query = "SELECT name, email, law_firm, expertise, exprience FROM lawyers WHERE id = ?"
    cursor.execute(query, (lawyer_id,))
    lawyer_data = cursor.fetchone()
    connection.close()

    if not lawyer_data:
        flash('Lawyer not found!', 'error')
        return redirect(url_for('lawyer_dashboard'))

    lawyer = {
        'name': lawyer_data[0],
        'email': lawyer_data[1],
        'license': lawyer_data[2],
        'expertise': lawyer_data[3],
        'exprience': lawyer_data[4]
    }
    return render_template('lawyer_profile.html', lawyer=lawyer)

    
@app.route('/lawyer_register',methods=['GET','POST'])
def lawyer_register():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        law_firm = request.form.get('law_firm')
        expertise = request.form.get('expertise')
        password = request.form.get('password')
        exprience= request.form.get('exprience')
        
        if password != password:
            return "Passwords do not match."
        
        conn = connect_to_database()
        cursor = conn.cursor()
        try:
            # Create clients table if it doesn't exist
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS lawyers (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    email TEXT NOT NULL,
                    law_firm TEXT NOT NULL,
                    expertise TEXT NOT NULL,
                    password TEXT NOT NULL,
                    exprience TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            ''')

            # Insert user data into the database
            #query = "INSERT INTO clients (username, name,cnfpas,paswd, gender, email, number) VALUES (?,?,?,?,?,?,?)"

            #cursor.execute(query, (username, name,cnfpas, paswd, gender, email, number))  # Added parameters for the query
            #conn.commit()  # Commit the transaction

            cursor.execute('''
        INSERT INTO lawyers (name,email,law_firm, expertise,password,exprience)
        VALUES (?, ?, ?, ?, ?,?)
        ''', ( name, email,law_firm,expertise,password,exprience))
            
            conn.commit()
            
            # Verify if the data is inserted correctly
            cursor.execute("SELECT * FROM lawyers WHERE email = ?", (email,))
            user = cursor.fetchone()

            if user:
                return redirect(url_for('lawyer_login'))
            else:
                return "Registration failed. Please try again."
        except Exception as e:
            conn.rollback()  # Rollback in case of an error
            print(f"An error occurred: {e}")  # Log the exact error for debugging
            return f"An error occurred: {e}"
        finally:
            cursor.close()
            conn.close()
        
    return render_template('lawyer_register.html')

@app.route('/lawyer_login', methods=['POST', 'GET'])
def lawyer_login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        # Connect to the database
        connection = sqlite3.connect('lawfirm.db')
        cursor = connection.cursor()
        query = "SELECT id FROM lawyers WHERE email = ? AND password = ?"
        cursor.execute(query, (email, password))
        lawyer = cursor.fetchone()
        connection.close()
        
        if lawyer:
            # Save lawyer ID in session
            session['lawyer_id'] = lawyer[0]  
            flash('Login successful!', 'success')
            
            # Redirect to the intended page (default to dashboard if not specified)
            next_page = request.args.get('next', 'new_dashboard')
            return redirect(url_for(next_page))
        else:
            flash('Invalid credentials.', 'error')
            return render_template('lawyer_login.html')
    
    # Save the next page to redirect after login
    next_page = request.args.get('next', None)
    return render_template('lawyer_login.html', next=next_page)



@app.route('/laywer_dashboard')
def dashboard():
    return render_template('lawyer_dashboard.html')

def connect_to_database():
    conn = sqlite3.connect('lawfirm.db')
    conn.row_factory = sqlite3.Row  # Allows accessing columns by name in the template
    return conn

@app.route('/client_management', methods=['GET', 'POST'])
def client_management():
    conn = connect_to_database()
    clients = []

    # Handle form submission for adding new clients
    if request.method == 'POST':
        name = request.form.get['name']
        email = request.form.get['email']
        number = request.form.get['number']

        # Insert new client data into the database
        try:
            conn.execute('INSERT INTO clients (name, email, number) VALUES (?, ?, ?)', (name, email, number))
            conn.commit()
        except Exception as e:
            print(f"An error occurred while inserting a client: {e}")

    # Fetch all clients from the database
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM clients")
        clients = cursor.fetchall()
    except Exception as e:
        print(f"An error occurred while fetching clients: {e}")
    finally:
        cursor.close()
        conn.close()

    # Render the template with the clients data
    return render_template('client_management.html', clients=clients)

# Route to delete a client
@app.route('/client_management/delete/<int:client_id>')
def delete_client(client_id):
    conn = connect_to_database()
    try:
        conn.execute('DELETE FROM clients WHERE id = ?', (client_id,))
        conn.commit()
        del_count+=1
    except Exception as e:
        print(f"An error occurred while deleting a client: {e}")
    finally:
        conn.close()
    return redirect(url_for('client_management'))

# Function to connect to the database
def connect_to_database():
    conn = sqlite3.connect('lawfirm.db')
    conn.row_factory = sqlite3.Row  # Allows accessing columns by name in the template
    return conn

@app.route('/apointment_management', methods=['GET', 'POST'])
def appointment_management():
    conn = connect_to_database()
    appointments = []

    # Handle form submission for adding new appointments
    if request.method == 'POST':
        client_name = request.form['client_name']
        date = request.form['date']
        time = request.form['time']
        status = request.form['status']

        # Insert new appointment data into the bookings table
        try:
            conn.execute(
                'INSERT INTO bookings (client_name, date, time, status) VALUES (?, ?, ?, ?)',
                (client_name, date, time, status)
            )
            conn.commit()
        except Exception as e:
            print(f"An error occurred while inserting an appointment: {e}")

    # Fetch all appointments from the bookings table
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM bookings")
        appointments = cursor.fetchall()
    except Exception as e:
        print(f"An error occurred while fetching appointments: {e}")
    finally:
        cursor.close()
        conn.close()

    # Render the template with the appointments data
    return render_template('apointment_management.html', appointments=appointments)

# Route to delete an appointment by ID
@app.route('/delete_appointment/<int:appointment_id>', methods=['GET'])
def delete_appointment(appointment_id):
    global del_count
    conn = get_db_connection()
    conn.execute('DELETE FROM bookings WHERE id = ?', (appointment_id,))
    conn.commit()
    conn.close()
    del_count += 1
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO del_counts (count_value) VALUES (?)', (del_count,))
        print("Delete count successfully inserted into del_counts table.")
        conn.commit()
    except Exception as e:
        print(f"An error occurred while storing the delete count: {e}")
    finally:
        cursor.close()
        conn.close()
    return redirect(url_for('appointment_management'))  # Redirect to appointment management page

def get_db_connection():
    conn = sqlite3.connect('lawfirm.db')  # Path to your database
    conn.row_factory = sqlite3.Row  # Allow access to columns by name
    return conn

# Route to fetch messages for the lawyer dashboard
DATABASE = 'lawfirm.db'

# Helper function to query the database
def query_db(query, args=(), one=False):
    """
    Execute a query against the database.

    :param query: The SQL query string
    :param args: Tuple of arguments for parameterized query
    :param one: If True, fetch only one result
    :return: Fetched results (one or all)
    """
    with sqlite3.connect(DATABASE) as conn:
        cur = conn.cursor()
        cur.execute(query, args)
        rv = cur.fetchall()
        conn.commit()
        return (rv[0] if rv else None) if one else rv

# Route to manage lawyer messages
# Database connection helper
def get_db_connection():
    conn = sqlite3.connect('lawfirm.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/message_management', methods=['GET', 'POST'])
def message_management():
    lawyer_id = 1  # Dummy lawyer ID, replace with session logic if needed
    receiver_id = 2  # Default client ID

    if request.method == 'POST':
        # Retrieve form data
        sender_id = request.form.get('sender_id')
        sender_role = request.form.get('sender_role')
        receiver_id = request.form.get('receiver_id')
        receiver_role = request.form.get('receiver_role')
        message = request.form.get('message')

        # Validate required fields
        if not sender_id or not receiver_id or not message:
            return "Error: Missing required fields", 400

        try:
            # Convert IDs to integers
            sender_id = int(sender_id)
            receiver_id = int(receiver_id)

            # Insert message into database
            conn = get_db_connection()
            conn.execute(
                '''
                INSERT INTO messages (sender_id, receiver_id, sender_role, receiver_role, message, timestamp)
                VALUES (?, ?, ?, ?, ?, ?)
                ''',
                (sender_id, receiver_id, sender_role, receiver_role, message, datetime.now())
            )
            conn.commit()
            conn.close()
        except Exception as e:
            return f"An error occurred while saving the message: {e}", 500

    # Retrieve conversation messages
    try:
        conn = get_db_connection()
        messages = conn.execute(
            '''
            SELECT sender_id, receiver_id, sender_role, receiver_role, message, timestamp
            FROM messages
            WHERE (sender_id = ? AND receiver_id = ?)
               OR (sender_id = ? AND receiver_id = ?)
            ORDER BY timestamp ASC
            ''',
            (lawyer_id, receiver_id, receiver_id, lawyer_id)
        ).fetchall()
        conn.close()
    except Exception as e:
        return f"An error occurred while fetching messages: {e}", 500

    # Render chat interface
    return render_template(
        'message_management.html',
        user_id=lawyer_id,
        role='lawyer',
        receiver_id=receiver_id,
        receiver_role='client',
        messages=messages
    )
    # Fetch all messages where the lawyer is involved (either sender or receiver)
    
# Route to fetch messages
"""@app.route('/messages', methods=['GET'])
def get_messages():
    sender_id = request.args.get('sender_id')
    receiver_id = request.args.get('receiver_id')

    conn = get_db_connection()
    messages = conn.execute('''
        SELECT * FROM messages 
        WHERE (sender_id = ? AND receiver_id = ?) 
           OR (sender_id = ? AND receiver_id = ?)
        ORDER BY timestamp
    ''', (sender_id, receiver_id, receiver_id, sender_id)).fetchall()

    messages_list = [
        {
            'id': message['id'],
            'sender': 'client' if message['sender_id'] == sender_id else 'lawyer',
            'text': message['text'],
            'time': datetime.strptime(message['timestamp'], '%Y-%m-%d %H:%M:%S').strftime('%I:%M %p')
        } for message in messages
    ]

    conn.close()
    return jsonify(messages_list)"""

@app.route('/enquiry_management', methods=['GET'])
def enquiry_management():
    conn = get_db_connection()                                              
    enquiries = conn.execute('SELECT * FROM contact').fetchall()  # Adjust this query based on your contact table structure
    conn.close()
    return render_template('enquiry_management', enquiries=enquiries)

@app.route('/delete_enquiry/<int:enquiry_id>', methods=['POST'])
def delete_enquiry(enquiry_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM contact WHERE id = ?', (enquiry_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('enquiry_management'))


UPLOAD_FOLDER = 'path/to/upload/folder'  # Specify the upload folder
ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx', 'jpg', 'png'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


#app = Flask(__name__)
#app.secret_key = 'your_secret_key'  # Replace with your secret key
#login_manager = LoginManager()
#login_manager.init_app(app)

#@login_manager.user_loader
# Define the path to the upload folder

# Folder where documents will be stored
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'pdf', 'docx', 'txt', 'jpg', 'png'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Check if the file extension is allowed
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# Assuming you have a function to get the database connection
def get_db_connection():
    import sqlite3
    conn = sqlite3.connect('lawfirm.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/upload_document', methods=['GET', 'POST'])
def upload_document():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        # Secure the filename before saving
        filename = secure_filename(file.filename)
        file.save(os.path.join('uploads', filename))

        # Now store the document details in the database
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO documents (filename, upload_date)
            VALUES (?, ?)
        ''', (filename, datetime.now()))
        conn.commit()
        conn.close()

        flash('File successfully uploaded and stored in database!')
        return redirect(url_for('view_documents'))

    return render_template('upload_document')

@app.route('/view_documents')
def view_documents():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM documents ORDER BY upload_date DESC')
    documents = cursor.fetchall()
    conn.close()
    return render_template('view_documents.html', documents=documents)

@app.route('/delete_document/<int:document_id>')
def delete_document(document_id):
    connection = sqlite3.connect('lawfirm.db')
    cursor = connection.cursor()

    # Get the document path from the database before deleting
    cursor.execute("SELECT document_path FROM documents WHERE id = ?", (document_id,))
    document = cursor.fetchone()

    if document:
        os.remove(document[0])  # Delete the document file from the server

        # Delete the document from the database
        cursor.execute("DELETE FROM documents WHERE id = ?", (document_id,))
        connection.commit()

    connection.close()

    return redirect(url_for('view_documents'))  # Redirect back to the view documents page


# Function to fetch notifications from the database
def get_notifications():
    conn = sqlite3.connect('lawfirm.db')  # Connect to your database
    cursor = conn.cursor()
    cursor.execute("SELECT id, message, timestamp, seen FROM notifications ORDER BY timestamp DESC")
    notifications = [
        {"id": row[0], "message": row[1], "timestamp": row[2], "seen": bool(row[3])}
        for row in cursor.fetchall()
    ]
    conn.close()
    return notifications

# Route to display notifications
@app.route('/notifications')
def notifications():
    notifications_list = get_notifications()
    return render_template('notifications.html', notifications=notifications_list)

@app.route('/mark_as_read/<int:notification_id>', methods=['POST'])
def mark_as_read(notification_id):
    conn = sqlite3.connect('lawfirm.db')
    cursor = conn.cursor()

    # Update the notification to be marked as seen
    cursor.execute('''
        UPDATE notifications 
        SET seen = 1 
        WHERE id = ?
    ''', (notification_id,))
    
    conn.commit()
    conn.close()

    # Redirect back to the notifications page
    return redirect(url_for('notifications'))

@app.route('/delete_notification/<int:notification_id>', methods=['POST'])
def delete_notification(notification_id):
    conn = sqlite3.connect('lawfirm.db')
    cursor = conn.cursor()

    # Delete the notification from the database
    cursor.execute('''
        DELETE FROM notifications 
        WHERE id = ?
    ''', (notification_id,))
    
    conn.commit()
    conn.close()

    # Redirect back to the notifications page after deletion
    return redirect(url_for('notifications'))


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect('lawfirm.db')
    return db

@app.route('/case_notes', methods=['GET'])
def view_case_notes():
    cursor = get_db().cursor()
    cursor.execute("SELECT * FROM case_notes")
    notes = cursor.fetchall()
    return render_template('case_notes.html', notes=notes)

@app.route('/case_notes/add', methods=['POST'])
def add_case_note():
    note_content = request.form['note']
    lawyer_id = request.form['lawyer_id']
    case_id = request.form['case_id']
    cursor = get_db().cursor()
    cursor.execute("INSERT INTO case_notes (lawyer_id, case_id, note) VALUES (?, ?, ?)", (lawyer_id, case_id, note_content))
    get_db().commit()
    return redirect(url_for('view_case_notes'))

@app.route('/case_notes/edit/<int:note_id>', methods=['POST'])
def edit_case_note(note_id):
    note_content = request.form['note']
    cursor = get_db().cursor()
    cursor.execute("UPDATE case_notes SET note = ? WHERE id = ?", (note_content, note_id))
    get_db().commit()
    return redirect(url_for('view_case_notes'))

@app.route('/case_notes/delete/<int:note_id>', methods=['POST'])
def delete_case_note(note_id):
    cursor = get_db().cursor()
    cursor.execute("DELETE FROM case_notes WHERE id = ?", (note_id,))
    get_db().commit()
    return redirect(url_for('view_case_notes'))

def get_db_connection():
    conn = sqlite3.connect('lawfirm.db')
    conn.row_factory = sqlite3.Row  # Allows us to return rows as dictionaries
    return conn

# Function to connect to the database
def get_db_connection():
    conn = sqlite3.connect('lawfirm.db')
    conn.row_factory = sqlite3.Row
    return conn

# Route for displaying the calendar
@app.route('/calendar')
def calendar():
    conn = get_db_connection()
    appointments = conn.execute('SELECT * FROM appointments').fetchall()
    conn.close()
    return render_template('calendar.html', appointments=appointments)

# Route for adding appointments
@app.route('/add_appointment', methods=['POST'])
def add_appointment():
    title = request.form['title']
    date = request.form['date']
    time = request.form['time']

    conn = get_db_connection()
    conn.execute('INSERT INTO appointments (title, date, time) VALUES (?, ?, ?)', (title, date, time))
    conn.commit()
    conn.close()

    return redirect(url_for('calendar'))

@app.route('/knowledge_base')
def knowledge_base():
    return render_template('knowledge_base.html')

#@app.route('/send_message', methods=["POST", "GET"])
#def home_new():
    """session.clear()  # Clear session to reset any previous room and name data
    if request.method == "POST":
        name = request.form.get("name")
        code = request.form.get("code")
        join = request.form.get("join", False)
        create = request.form.get("create", False)

        if not name:
            flash("Please enter a name.")
            return render_template("jake.html", code=code, name=name)

        if join and not code:
            flash("Please enter a room code.")
            return render_template("jake.html", code=code, name=name)

        if create:
            code = generate_unique_code(4)
            rooms[code] = {"members": 0, "messages": []}
        elif code not in rooms:
            flash("Room does not exist.")
            return render_template("text.html", code=code, name=name)

        session["room"] = code
        session["name"] = name
        return redirect(url_for("room"))"""

    return render_template("send_message.html")

"""@app.route("/send_message")
def room():
    room = session.get("room")
    if room is None or session.get("name") is None or room not in rooms:
        return redirect(url_for("jake"))
   #return render_template("send_message.html", code=room, messages=rooms[room]["messages"])

# Socket event for handling messages
@socketio.on("message")
def message(data):
    room = session.get("room")
    if room not in rooms:
        return

    content = {"name": session.get("name"), "message": data["data"]}
    send(content, to=room)
    rooms[room]["messages"].append(content)
    print(f"{session.get('name')} said: {data['data']}")

# Socket event for new connections
@socketio.on("connect")
def connect(auth):
    room = session.get("room")
    name = session.get("name")
    if not room or not name:
        return
    if room not in rooms:
        leave_room(room)
        return

    join_room(room)
    send({"name": name, "message": "has entered the room"}, to=room)
    rooms[room]["members"] += 1
    print(f"{name} joined room {room}")

# Socket event for disconnections
@socketio.on("disconnect")
def disconnect():
    room = session.get("room")
    name = session.get("name")
    leave_room(room)

    if room in rooms:
        rooms[room]["members"] -= 1
        if rooms[room]["members"] <= 0:
            del rooms[room]

    send({"name": name, "message": "has left the room"}, to=room)
    print(f"{name} has left the room {room}")"""

DATABASE = 'lawfirm.db'

# Helper function to connect to the database
def db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

# Route to send a message (common for both lawyer and client)
# Database connection function
def connect_db():
    conn = sqlite3.connect('lawfirm.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/send_message', methods=['POST'])
def send_message():
    try:
        # Get form data
        sender_id = int(request.form['sender_id'])
        receiver_id = int(request.form['receiver_id'])
        sender_role = request.form['sender_role']
        receiver_role = request.form['receiver_role']
        message = request.form['message']

        # Ensure message is not empty
        if not message.strip():
            return "Message cannot be empty", 400

        # Insert message into database
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO messages (sender_id, receiver_id, sender_role, receiver_role, message, timestamp)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (sender_id, receiver_id, sender_role, receiver_role, message, datetime.now()))
        conn.commit()
        conn.close()

        # Redirect back to the chat page (adjust as needed)
        return redirect(url_for('send_message_page'))  # Replace with the correct page name

    except Exception as e:
        return f"An error occurred: {e}", 500

# Example route for rendering the chat page
@app.route('/send_message')
def send_message_page():
    # Fetch messages from the database
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM messages ORDER BY timestamp ASC')
    messages = cursor.fetchall()
    conn.close()

    return render_template('send_message.html', messages=messages, user_id=1, role='client')  # Adjust user_id and role


# Route to view chat messages
@app.route('/chat/<role>/<int:user_id>', methods=['GET'])
def view_chat(role, user_id):
    conn = db_connection()
    cursor = conn.cursor()

    if role == 'lawyer':
        query = """
            SELECT * FROM messages
            WHERE receiver_id = ? AND receiver_role = 'lawyer'
            ORDER BY timestamp ASC
        """
    elif role == 'client':
        query = """
            SELECT * FROM messages
            WHERE receiver_id = ? AND receiver_role = 'client'
            ORDER BY timestamp ASC
        """
    messages = cursor.execute(query, (user_id,)).fetchall()
    conn.close()

    return render_template('send_message.html', messages=messages, user_id=user_id, role=role)

# Home route to redirect to chat for demo purposes
@app.route('/')
def home_come():
    return redirect(url_for('view_chat', role='client', user_id=1))  # Replace with dynamic user ID and role
@app.route('/applications')
def show_applications():
    connection = sqlite3.connect('lawfirm.db')
    cursor = connection.cursor()
    
    # Fetch all applications from the job_applications table
    cursor.execute("SELECT id, name, email, position, created_at FROM job_application")
    applications = cursor.fetchall()
    
    connection.close()
    
    # Pass the fetched applications to the template
    return render_template('applications.html', applications=applications)


def get_db_connection():
    conn = sqlite3.connect('lawfirm.db',timeout=2000)  # Your database file
    conn.row_factory = sqlite3.Row  # To access columns by name
    return conn

# Route to display invoices and the billing overview
@app.route('/billing_invoicing')
def billing_invoicing():
    conn = sqlite3.connect('lawfirm.db')
    conn.row_factory = sqlite3.Row  # This allows the database rows to be accessed by column name
    cursor = conn.cursor()

    # Fetch all invoices as dictionaries
    cursor.execute("SELECT id, client_name, total_amount, amount_paid, status FROM invoices")
    invoices = cursor.fetchall()

    conn.close()
    return render_template('billing_invoicing.html', invoices=invoices)


@app.route('/add_invoice', methods=['POST'])
def add_invoice():
    client_name = request.form['client_name']
    total_amount = float(request.form['total_amount'])
    status = request.form['status']
    
    # Connect to the database
    conn = sqlite3.connect('lawfirm.db')
    cursor = conn.cursor()
    
    # Insert the new invoice into the database
    cursor.execute("""
        INSERT INTO invoices (client_name, total_amount, amount_paid, status)
        VALUES (?, ?, 0, ?)
    """, (client_name, total_amount, status))
    
    conn.commit()
    conn.close()
    
    return redirect(url_for('billing_invoicing'))

@app.route('/make_payment/<int:invoice_id>', methods=['POST'])
def make_payment(invoice_id):
    installment_str = request.form['installment']
    if not installment_str:
        return "Installment amount is required.", 400
    try:
        installment = float(installment_str)
    except ValueError:
        return "Invalid installment amount.", 400
    
    # Connect to the database
    conn = sqlite3.connect('lawfirm.db')
    cursor = conn.cursor()
    
    # Fetch the invoice details
    cursor.execute("SELECT total_amount, amount_paid FROM invoices WHERE id = ?", (invoice_id,))
    invoice = cursor.fetchone()

    if invoice:
        total_amount, amount_paid = invoice
        new_amount_paid = amount_paid + installment
        remaining_balance = total_amount - new_amount_paid
        
        # Update the invoice with the new amount paid
        cursor.execute("""
            UPDATE invoices
            SET amount_paid = ?, remaining_balance = ?
            WHERE id = ?
        """, (new_amount_paid, remaining_balance, invoice_id))
        
        conn.commit()

    conn.close()
    
    return redirect(url_for('billing_invoicing'))

# Route to delete an invoice
@app.route('/delete_invoice/<int:invoice_id>', methods=['GET', 'POST'])
def delete_invoice(invoice_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM invoices WHERE id = ?', (invoice_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('billing_invoicing'))

# Route to update the status of an invoice
def get_invoice_by_id(invoice_id):
    conn = sqlite3.connect('lawfirm.db')  # Your SQLite database
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM invoices WHERE id = ?", (invoice_id,))
    invoice = cursor.fetchone()  # Fetch the first matching record
    conn.close()
    return invoice

# Function to update the invoice in the database
def update_invoice_in_db(invoice_id, total_amount, amount_paid, remaining_balance, status):
    conn = sqlite3.connect('lawfirm.db')  # Your SQLite database
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE invoices 
        SET total_amount = ?, amount_paid = ?, remaining_balance = ?, status = ?
        WHERE id = ?
    """, (total_amount, amount_paid, remaining_balance, status, invoice_id))
    conn.commit()
    conn.close()


@app.route('/update_invoice/<int:invoice_id>', methods=['GET', 'POST'])
def update_invoice(invoice_id):
    # Fetch the invoice from the database using the function
    invoice = get_invoice_by_id(invoice_id)
    
    if request.method == 'POST':
        # Get form data and ensure numeric conversion
        total_amount = float(request.form['total_amount'])
        amount_paid = float(request.form['amount_paid'])
        remaining_balance = total_amount - amount_paid
        status = request.form['status']

        # Update the invoice in the database using the update function
        update_invoice_in_db(invoice_id, total_amount, amount_paid, remaining_balance, status)
        return redirect(url_for('billing_invoicing'))  # Redirect to the billing page after update

    # If GET request, render the update invoice form with the invoice data
    return render_template('update_invoice.html', invoice=invoice)

    # If GET request, render the update invoice form
    return render_template('update_invoice.html', invoice=invoice)


@app.route('/payment', methods=['GET', 'POST'])
def payment():
    if request.method == 'POST':
        # Capture form data
        payment_amount = request.form['payment_amount']
        # Process payment logic here (payment gateway integration)

        # Update database after successful payment
        # Redirect to a success page or back to the dashboard
        return redirect(url_for('billing_invoicing'))
    else:
        # Render the payment page with outstanding balance
        outstanding_balance = 5000  # Example balance
        return render_template('payment.html', outstanding_balance=outstanding_balance)
    
DATABASE = 'lawfirm.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

# Function to create the `qr_payment` table
def create_tables():
    conn = get_db_connection()
    conn.execute('''CREATE TABLE IF NOT EXISTS qr_payment (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    transaction_id TEXT NOT NULL,
                    name TEXT NOT NULL,
                    date TEXT NOT NULL,
                    time TEXT NOT NULL)''')
    conn.commit()
    conn.close()

# Route to display the QR payment form
@app.route('/qr_payment', methods=['GET', 'POST'])
def qr_payment():
    if request.method == 'POST':
        transaction_id = request.form['transaction_id']
        name = request.form['name']
        date = request.form['date']
        time = request.form['time']
        
        # Store the payment details in the database
        conn = get_db_connection()
        conn.execute('INSERT INTO qr_payment (transaction_id, name, date, time) VALUES (?, ?, ?, ?)',
                     (transaction_id, name, date, time))
        conn.commit()
        conn.close()
        
        # Return success response in JSON format for JavaScript handling
        return jsonify(success=True)
    
    return render_template('qr_payment.html')



# Route to render Task Management page and display tasks
@app.route('/task_management', methods=['GET'])
def task_management():
    conn = get_db_connection()
    tasks = conn.execute('SELECT * FROM tasks').fetchall()
    conn.close()
    return render_template('task_management.html', tasks=tasks)

# Route to add a new task via a form submission
@app.route('/add_task', methods=['POST'])
def add_task():
    title = request.form['title']
    description = request.form.get('description', '')
    deadline = request.form.get('deadline', '')

    conn = get_db_connection()
    conn.execute(
        'INSERT INTO tasks (title, description, deadline) VALUES (?, ?, ?)',
        (title, description, deadline)
    )
    conn.commit()
    conn.close()
    return redirect(url_for('task_management'))

# Route to update an existing task via a form submission
@app.route('/update_task/<int:task_id>', methods=['GET', 'POST'])
def update_task(task_id):
    conn = get_db_connection()
    task = conn.execute('SELECT * FROM tasks WHERE id = ?', (task_id,)).fetchone()

    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        deadline = request.form['deadline']
        status = request.form['status']
        
        conn.execute('''
            UPDATE tasks
            SET title = ?, description = ?, deadline = ?, status = ?
            WHERE id = ?
        ''', (title, description, deadline, status, task_id))
        conn.commit()
        conn.close()
        return redirect(url_for('task_management'))

    conn.close()
    return render_template('update_task.html', task=task)

# Route to delete a task
@app.route('/delete_task/<int:task_id>', methods=['POST'])
def delete_task(task_id):
    conn = sqlite3.connect('lawfirm.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
    conn.commit()
    conn.close()

    return redirect(url_for('task_management'))

@app.route('/help')
def help():
    return render_template('help.html')

@app.route('/lawyer_help')
def lawyer_help():
    return render_template('lawyer_help.html')
@app.route('/user')
def user(): 
    if 'username' not in session:
        return redirect(url_for('login'))
    return redirect(url_for('profile'))
    return render_template('user.html', user=user)


@app.route('/logout')
def logout():
    session.clear()  # Clear all session data
    return redirect(url_for('login'))  # Redirect to the login page


@app.route('/update_profile', methods=['GET', 'POST'])
def update_profile():
    if 'user_id' not in session:
        # Store the intended page in the session for redirecting later
        session['next'] = request.url
        return redirect('/login')

    user_id = session['user_id']  # Retrieve user ID from session

    if request.method == 'POST':
        # Retrieve form data
        username = request.form.get('username', '').strip()
        name = request.form.get('name', '').strip()
        paswd = request.form.get('paswd', '').strip()
        cnfpas = request.form.get('cnfpas', '').strip()
        gender = request.form.get('gender', '').strip()
        email = request.form.get('email', '').strip()
        number = request.form.get('number', '').strip()

        # Validate form data
        if not username or not name or not email or not number or not paswd or not cnfpas:
            return "All fields are required."
        if paswd != cnfpas:
            return "Passwords do not match."

        try:
            conn = connect_to_database()
            cursor = conn.cursor()

            # Update user details in the database
            query = """
                UPDATE clients
                SET username = ?, name = ?, paswd = ?, cnfpas = ?, gender = ?, email = ?, number = ?
                WHERE id = ?
            """
            cursor.execute(query, (username, name, paswd, cnfpas, gender, email, number, user_id))
            conn.commit()

            # Confirm successful update
            print(f"Profile updated successfully for user ID {user_id}.")
        except Exception as e:
            print(f"Error updating profile: {e}")
            return "An error occurred while updating your profile. Please try again."
        finally:
            cursor.close()
            conn.close()

        # Update session with new values
        session['username'] = username
        session['name'] = name
        session['email'] = email
        session['number'] = number

        return redirect(url_for('user'))

    # Fetch current user data to prefill the form
    try:
        conn = connect_to_database()
        cursor = conn.cursor()
        cursor.execute("SELECT username, name, gender, email, number FROM clients WHERE id = ?", (user_id,))
        user_data = cursor.fetchone()
    except Exception as e:
        print(f"Error fetching user data: {e}")
        return "An error occurred while loading your profile. Please try again."
    finally:
        cursor.close()
        conn.close()

    # Render the form with prefilled data
    return render_template('edit_profile.html', user=user_data)

@app.route('/apointment_by_lawyer', methods=['GET', 'POST'])
def appointment_by_lawyer():
    if request.method == 'POST':
        # Get form data
        name = request.form['name']
        lawyer_type = request.form['lawyer_type']
        email = request.form['email']
        case_description = request.form['case_description']
        appointment_date = request.form['appointment_date']
        time_of_booking = request.form['time_of_booking']
        date_of_booking = request.form['date_of_booking']
        username = request.form['username']  # Added field for username

        # Validate that the inputs are not empty
        if not appointment_date or not time_of_booking or not date_of_booking or not username:
            return "All fields are required."
        
        # Store booking details in the database
        try:
            conn = sqlite3.connect('lawfirm.db')
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO bookings 
                (name, lawyer_type, email, case_description, appointment_date, time_of_booking, date_of_booking, username) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (name, lawyer_type, email, case_description, appointment_date, time_of_booking, date_of_booking, username))
            
            # Assuming notifications are still part of your system, you could also notify here:
            cursor.execute('''
                INSERT INTO notifications (user_id, message) 
                VALUES (?, ?)
            ''', (username, 'New booking for lawyer: {} by {} at {}'.format(lawyer_type, name, appointment_date)))
            conn.commit()
            conn.close()
            
            return redirect(url_for('appointment_management'))  # Redirect after successful submission
        except Exception as e:
            return f"An error occurred: {e}"

    # If GET request, render the appointment form page
    return render_template('apointment_by_lawyer.html')

# Database connection function
def get_db_connection():
    conn = sqlite3.connect('lawfirm.db')  # Replace 'lawfirm.db' with your database name
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/create_case', methods=['GET', 'POST'])
def create_case():
    if request.method == 'POST':
        # Get form data from the request
        case_name = request.form.get('case_name')
        client_name = request.form.get('client_name')
        start_date = request.form.get('start_date')
        status = request.form.get('status')
        description = request.form.get('description')

        try:
            # Connect to the database
            conn = sqlite3.connect('lawfirm.db')
            cursor = conn.cursor()

            # Insert the new case into the 'cases' table
            cursor.execute('''
                INSERT INTO cases (case_name, client_name, start_date, status, description)
                VALUES (?, ?, ?, ?, ?)
            ''', (case_name, client_name, start_date, status, description))

            # Commit the transaction and close the connection
            conn.commit()
            conn.close()

            # Redirect to the same page with a success parameter
            return redirect(url_for('create_case', success='true'))
        except Exception as e:
            print(f"Error: {e}")
            # Redirect to the same page with a failure parameter
            return redirect(url_for('create_case', success='false'))

    # Render the Create Case page
    return render_template('create_case.html')

# Route to render the case updates page
@app.route('/case_update/<int:case_id>', methods=['GET', 'POST'])
def case_update(case_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == 'POST':
        # Retrieving form data
        case_name = request.form['case_name']
        client_name = request.form['client_name']
        start_date = request.form['start_date']
        status = request.form['status']
        description = request.form['description']

        # Update the case in the database
        cursor.execute('''
            UPDATE cases
            SET case_name = ?, client_name = ?, start_date = ?, status = ?, description = ?
            WHERE case_id = ?
        ''', (case_name, client_name, start_date, status, description, case_id))

        conn.commit()
        conn.close()

        # Redirect to the updated case page or a list of cases
        return redirect(url_for('case_list'))  # Adjust as needed to your case listing page

    # If GET request, fetch the case data to populate the form
    case = cursor.execute('SELECT * FROM cases WHERE case_id = ?', (case_id,)).fetchone()
    conn.close()

    if case is None:
        return "Case not found", 404  # Or redirect to an error page

    return render_template('case_update.html', case=case)
# Example case list route
@app.route('/case_list')
def case_list():
    conn = get_db_connection()
    cases = conn.execute('SELECT * FROM cases').fetchall()
    conn.close()
    return render_template('case_list.html', cases=cases)


@app.route('/create_document', methods=['GET', 'POST'])
def create_document():
    if request.method == 'POST':
        document_content = request.form.get('document_content')  # Text from Quill editor

        # Save document to database or filesystem
        with open('document.txt', 'w') as f:
            f.write(document_content)

        return redirect(url_for('view_document'))

    return render_template('document_editor.html')


@app.route('/view_document')
def view_document():
    # You can use this route to render saved documents or view them.
    try:
        with open('document.txt', 'r') as f:
            document_content = f.read()
    except FileNotFoundError:
        document_content = "No document found."
    
    return render_template('view_document.html', content=document_content)


@app.route('/generate_pitison', methods=['GET', 'POST'])
def generate_pitison():
    if request.method == 'POST':
        name = request.form['name']
        town = request.form['town']
        district = request.form['district']
        state = request.form['state']
        contact = request.form['contact']

        # Generate Pitison content dynamically
        pitison_content = f"This Pitison is filed by {name}, residing at {town}, {district}, {state}. The contact number is {contact}."

        # You can render the generated content or return as a downloadable file
        return render_template('pitison.html', pitison_content=pitison_content)

    return render_template('pitison.html')


@app.route('/editor')
def editor():
    return render_template('editor.html')  # Where the lawyer can select a template

@app.route('/pitison')
def pitison():
    return render_template('pitison.html')  # Pitison form template

@app.route('/fir')
def fir():
    return render_template('fir.html')  # FIR form template

@app.route('/affidavit')
def affidavit():
    return render_template('affidavit.html')  # Affidavit form template

@app.route('/tracker')
def tracker():
    # Sample data (you will replace it with actual database queries)
    case_status = {'pending': 45, 'ongoing': 35, 'closed': 20}
    cases_by_lawyer = {'Lawyer 1': 10, 'Lawyer 2': 5, 'Lawyer 3': 8}
    overall_progress = {'completed': 60, 'in_progress': 40}
    
    return render_template('tracker_page.html', case_status=case_status, cases_by_lawyer=cases_by_lawyer, overall_progress=overall_progress)


UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf', 'docx'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/e_signature', methods=['GET', 'POST'])
def e_signature():
    if request.method == 'POST':
        file = request.files.get('file')
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return render_template('e_signature.html', document_filename=filename)
    return render_template('e_signature.html')

@app.route('/save_signature', methods=['POST'])
def save_signature():
    signature_data = request.form['signature']
    document = request.files.get('document')
    
    # Save the signature as an image
    signature_img = base64.b64decode(signature_data.split(',')[1])
    with open('signature.png', 'wb') as f:
        f.write(signature_img)

    # Here, you would merge the signature with the document, for example using PyPDF2
    if document:
        document_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(document.filename))
        document.save(document_path)

        # Example: merge signature with document using PyPDF2 (you would need to customize this part)
        reader = PdfReader(document_path)
        writer = PdfWriter()

        # Add pages from the document
        for page in reader.pages:
            writer.add_page(page)

        # Add signature to document (this is just a placeholder, replace with actual implementation)
        # You would need to use a library like reportlab or pdfrw to add the image to the PDF

        signed_filename = 'signed_' + document.filename
        with open(signed_filename, 'wb') as f:
            writer.write(f)

    return jsonify({"status": "success"})


# Database setup
DATABASE = "lawfirm.db"

def init_db():
    """Initialize the database."""
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS reviews (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                review TEXT NOT NULL,
                rating INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()

init_db()  # Initialize database when the server starts

# Routes
DATABASE = 'lawfirm.db'

# Database connection
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

# Create the reviews table if it doesn't exist
def init_db():
    with app.app_context():
        db = get_db()
        db.execute('''CREATE TABLE IF NOT EXISTS reviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            review TEXT NOT NULL,
            rating INTEGER CHECK(rating >= 1 AND rating <= 5)
        )''')
        db.commit()

@app.route('/reviews', methods=['GET', 'POST'])
def reviews():
    db = get_db()
    if request.method == 'POST':
        name = request.form['name']
        review = request.form['review']
        rating = request.form['rating']
        
        if not name or not review or not rating:
            return "All fields are required!", 400

        try:
            db.execute('INSERT INTO reviews (name, review, rating) VALUES (?, ?, ?)', (name, review, int(rating)))
            db.commit()
            return redirect(url_for('reviews'))
        except sqlite3.Error as e:
            return f"An error occurred: {e}", 500

    # Fetch all reviews for display
    cursor = db.execute('SELECT * FROM reviews ORDER BY id DESC')
    reviews_data = cursor.fetchall()
    return render_template('review.html', reviews=reviews_data)

@app.route('/new_video.html')
def new_video():
    return render_template('new_video.html')

# Route for the lawyer video interface
@app.route('/new_video_lawyer')
def new_video_lawyer():
    return render_template('new_video_lawyer.html')

# Connect to SQLite
def connect_to_database():
    return sqlite3.connect('lawfirm.db')

# Route to start the chat for client
@app.route('/whatsapp', methods=['GET', 'POST'])
def whatsapp():
    if 'user_id' not in session:
        return redirect(url_for('login'))  # Redirect to login if not logged in
    
    user_id = session['user_id']
    conn = connect_to_database()
    cursor = conn.cursor()
    
    # Fetch all chats between the user (client) and any lawyer
    cursor.execute("SELECT * FROM chats WHERE client_id = ?", (user_id,))
    chats = cursor.fetchall()
    conn.close()
    
    return render_template('whatsapp.html', chats=chats)

# Route for the lawyer to select a client and see their chat
@app.route('/meta', methods=['GET', 'POST'])
def meta():
    if 'lawyer_id' not in session:
        return redirect(url_for('lawyer_login'))  # Redirect to login if lawyer is not logged in
    
    if request.method == 'POST':
        client_username = request.form['client_username']  # Name of the client selected
        conn = connect_to_database()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM clients WHERE username = ?", (client_username,))
        client = cursor.fetchone()
        conn.close()
        
        if client:
            session['client_id'] = client[0]
            return redirect(url_for('chat_room', client_username=client_username)) # Redirect to chat room with the selected client
        else:
            return "Client not found", 404
    
    return render_template('meta.html')

@app.route('/chat_room/<client_username>', methods=['GET', 'POST'])
def chat_room(client_username):
    if 'lawyer_id' not in session:
        return redirect(url_for('lawyer_login'))  # Redirect if lawyer is not logged in
    
    lawyer_id = session['lawyer_id']

    # Get client information based on the username
    conn = connect_to_database()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM clients WHERE username = ?", (client_username,))
    client = cursor.fetchone()
    conn.close()

    if not client:
        flash("Client not found.", "error")
        return redirect(url_for('dashboard'))

    client_id = client[0]  # Get the client ID from the query result

    # Fetch all chats between the lawyer and the selected client from the database
    conn = connect_to_database()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM chats 
        WHERE (client_id = ? AND lawyer_id = ?) 
        OR (client_id = ? AND lawyer_id = ?)
        ORDER BY timestamp ASC
    """, (client_id, lawyer_id, lawyer_id, client_id))
    chats = cursor.fetchall()
    conn.close()

    # Handle message submission
    if request.method == 'POST':
        message = request.form['message']
        if message:
            # Insert new message into the database
            conn = connect_to_database()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO chats (client_id, lawyer_id, message) VALUES (?, ?, ?)", 
                           (client_id, lawyer_id, message))
            conn.commit()
            conn.close()

            # Redirect to the same chat room to refresh the messages
            return redirect(url_for('chat_room', client_username=client_username))

    # Return the template with the chats and client info
    return render_template('chat_room.html', chats=chats, client_username=client_username, lawyer_id=lawyer_id)

# SocketIO: Send message
@socketio.on('send_message')
def handle_message(data):
    message = data['message']
    sender_id = data['sender_id']
    recipient_id = data['recipient_id']
    sender_role = data['sender_role']
    
    # Save the message to the chats table
    conn = connect_to_database()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO chats (client_id, lawyer_id, message, sender_role) VALUES (?, ?, ?, ?)",
                   (sender_id if sender_role == 'client' else None, 
                    recipient_id if sender_role == 'lawyer' else None,
                    message, sender_role))
    conn.commit()
    conn.close()
    
    # Broadcast the message to the respective room (client-lawyer)
    room_id = f"{sender_id}-{recipient_id}"  # Create a room based on user IDs
    send(message, room=room_id)

# SocketIO: Connect to room
@socketio.on('join')
def on_join(data):
    room_id = data['room_id']
    join_room(room_id)

 # Book data (replace with your actual books and images)
books = [
    {
        "title": "ADMINISTRATIVE_LAW_FF",
        "author": "John Doe",
        "image": "static/images/constitutional.jpg",
        "link": "static/books/ADMINISTRATIVE_LAW_FF.pdf"
    },
    {
        "title": "ADVOCATES_ACT_f",
        "author": "Jane Smith",
        "image": "static/images/criminal.jpg",
        "link": "static/books/ADVOCATES_ACT_f.pdf"
    },
    {
        "title": "ANCIENT_LAW",
        "author": "Sam Wilson",
        "image": "static/images/contract.jpg",
        "link": "static/books/ANCIENT_LAW _F.pdf"
    },
    {
        "title": "ARBITRATION_And_CONCILIATION",
        "author": "Alice Brown",
        "image": "static/images/corporate.jpg",
        "link": "static/books/ARBITRATION_And_CONCILIATION.pdf"
    },
    {
        "title": "CIVIL_PROCEDURE_CODE_FINAL2012",
        "author": "Emma Stone",
        "image": "static/images/property.jpg",
        "link": "static/books/CIVIL_PROCEDURE_CODE_FINAL2012.pdf"
    },
    {
        "title": "COMPANY_LAW",
        "author": "Emma Stone",
        "image": "static/images/property.jpg",
        "link": "static/books/COMPANY_LAW.pdf"
    },
    {
        "title": "CONSTITUTION_OF_INDIA",
        "author": "Emma Stone",
        "image": "static/images/property.jpg",
        "link": "static/books/CONSTITUTION_OF_INDIA.pdf"
    },
    {
        "title": "CONTRACT_Act_F",
        "author": "Emma Stone",
        "image": "static/images/property.jpg",
        "link": "static/books/CONTRACT_Act_F.pdf"
    },
    {
        "title": "CRIMINAL_PROCEDURE_CODE",
        "author": "Emma Stone",
        "image": "static/images/property.jpg",
        "link": "static/books/CRIMINAL_PROCEDURE_CODE.pdf"
    },
    # Add 5 more books as needed
]

@app.route('/books')
def books_page():
    """
    Render the books page, passing the book data directly to the template.
    """
    return render_template('books.html', books=books)

@app.route('/law_book')
def law_books():
    """
    Render the books page, passing the book data directly to the template.
    """
    return render_template('law_book.html', books=books)

# Set your OpenAI API key
openai.api_key = "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"

@app.route('/chatbot', methods=['GET', 'POST'])
def chatbot():
    if request.method == 'POST':
        user_input = request.form['user_input']
        try:
            # Correct usage of the updated OpenAI API
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful AI lawyer."},
                    {"role": "user", "content": user_input}
                ]
            )
            reply = response['choices'][0]['message']['content'].strip()
        except Exception as e:
            reply = f"Error: {e}"
        return render_template('chatbot.html', user_input=user_input, reply=reply)
    return render_template('chatbot.html')

def fetch_random_case():
    connection = sqlite3.connect('lawfirm.db')  # Replace with your database name
    cursor = connection.cursor()

    # Get all case IDs from the dummy_cases table
    cursor.execute("SELECT id, case_title, case_description FROM dummy_cases")
    cases = cursor.fetchall()

    if not cases:
        connection.close()
        raise ValueError("No cases found in the database.")

    # Select a random case
    random_case = random.choice(cases)

    case_data = {
        "id": random_case[0],
        "case_title": random_case[1],
        "case_description": random_case[2]
    }

    connection.close()
    return case_data

def evaluate_argument(argument, case_id):
    """
    Evaluate the lawyer's argument and provide feedback.

    :param argument: The text of the lawyer's argument.
    :param case_id: The ID of the case being argued.
    :return: A dictionary containing the judge's question, the result of the case, and a rating.
    """
    import random

    # Simulated responses for demonstration
    responses = [
        {"result": "Bail Granted", "rating": random.randint(7, 10), 
         "judge_question": "How would you respond to the prosecution's claim about insufficient evidence?"},
        {"result": "Case Upheld", "rating": random.randint(5, 8), 
         "judge_question": "What precedents would you cite to strengthen your case?"},
        {"result": "Case Rejected", "rating": random.randint(3, 6), 
         "judge_question": "How can you counter the witness's testimony in this case?"}
    ]

    # Generate a response based on the argument and case
    response = random.choice(responses)

    return {
        "result": response["result"],
        "rating": response["rating"],
        "judge_question": response["judge_question"]
    }


def save_response(case_id, argument, result, rating, judge_question):
    """
    Save the lawyer's response and evaluation results into the database.

    :param case_id: The ID of the case being argued.
    :param argument: The text of the lawyer's argument.
    :param result: The outcome of the case (e.g., Bail Granted, Case Rejected).
    :param rating: The lawyer's performance rating.
    :param judge_question: The judge's follow-up question.
    """
    connection = sqlite3.connect('lawfirm.db')  # Ensure the database file exists
    cursor = connection.cursor()

    # Create the table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS lawyer_responses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            case_id INTEGER,
            argument TEXT,
            result TEXT,
            rating INTEGER,
            judge_question TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Insert the response into the table
    cursor.execute('''
        INSERT INTO lawyer_responses (case_id, argument, result, rating, judge_question)
        VALUES (?, ?, ?, ?, ?)
    ''', (case_id, argument, result, rating, judge_question))

    # Commit changes and close the connection
    connection.commit()
    connection.close()



def get_case_details(case_id):
    """
    Retrieve case details from the database by case ID.

    :param case_id: The ID of the case to retrieve.
    :return: A dictionary containing case details (title, description, etc.) or None if not found.
    """
    connection = sqlite3.connect('lawfirm.db')  # Ensure the database file exists
    cursor = connection.cursor()

    # Create the table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cases (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT NOT NULL
        )
    ''')

    # Fetch the case details
    cursor.execute('SELECT title, description FROM cases WHERE id = ?', (case_id,))
    case = cursor.fetchone()
    connection.close()

    # If case exists, return as a dictionary
    if case:
        return {"id": case_id, "title": case[0], "description": case[1]}
    else:
        return None

# Route to render the courtroom interface
@app.route('/courtroom')
def courtroom():
    # Fetch a random dummy case from the database
    case = fetch_random_case()  # Implement fetch_random_case()
    return render_template('courtroom.html', case=case)

# API for argument submission and AI response
@app.route('/submit_argument', methods=['POST'])
def submit_argument():
    argument = request.form.get('argument')
    case_id = int(request.form.get('case_id', 1))  # Default to 1 if not provided
    
    # Evaluate the argument
    response = evaluate_argument(argument, case_id)
    
    # Save the response in the database
    save_response(
        case_id=case_id,
        argument=argument,
        result=response["result"],
        rating=response["rating"],
        judge_question=response["judge_question"]
    )
    
    return jsonify(response)

 
def generate_ai_response(lawyer_argument, case_id):
    openai.api_key = 'YOUR_API_KEY'
    case_details = get_case_details(case_id)  # Fetch case details

    prompt = f"""
    You are a judge in a courtroom. A lawyer has presented this argument:
    {lawyer_argument}
    
    Based on the following case details:
    {case_details}
    
    Respond with a counterargument or a follow-up question.
    """
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "system", "content": prompt}]
    )
    return response['choices'][0]['message']['content']

@app.route('/get_case', methods=['GET'])
def get_case():
    case_id = int(request.args.get('case_id', 1))  # Default to 1 if not provided
    case_details = get_case_details(case_id)
    
    if case_details:
        return jsonify({"success": True, "case": case_details})
    else:
        return jsonify({"success": False, "message": "Case not found"}), 404
def seed_cases():
    connection = sqlite3.connect('lawfirm.db')
    cursor = connection.cursor()

    # Insert some dummy case data
    cursor.execute('INSERT INTO cases (title, description) VALUES (?, ?)', 
                   ("Theft Case", "A person is accused of stealing a bicycle."))
    cursor.execute('INSERT INTO cases (title, description) VALUES (?, ?)', 
                   ("Property Dispute", "Two neighbors are disputing the ownership of a piece of land."))
    
    connection.commit()
    connection.close()

@app.route('/new_dashboard')
def new_dashboard():
    global clients,delete
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM bookings')
    appointments = cursor.fetchall()
    total_bookings = len(appointments)
    cursor.execute('SELECT * FROM clients')
    clients = cursor.fetchall()
    total_clients=len(clients)
    cursor.execute('SELECT * FROM del_counts')
    delete=cursor.fetchall()
    total_deleted_records = len(delete)
    #fetch the id of the last booking 
    cursor.execute('SELECT id FROM bookings ORDER BY id DESC LIMIT 1')
    last_booking_id=cursor.fetchone()[0]
    #calculate completed bookings
    completed_bookings=last_booking_id-total_bookings
    #Count the total number of deleted data from bookings table
    #cursor.execute('SELECT COUNT(*) FROM bookings WHERE deleted = 1')
    #total_deleted_bookings = cursor.fetchone()[0]
    # Fetch the total number of deleted records from the del_counts table
    # Fetch the total number of clients from the clients table
    # Fetch the total number of tasks from the tasks table
# Fetch the total number of tasks from the tasks table
# Fetch the total number of tasks from the tasks table
    cursor.execute('SELECT COUNT(*) FROM tasks')
    total_tasks = cursor.fetchone()[0]

    # Fetch the number of pending tasks
    cursor.execute("SELECT COUNT(*) FROM tasks WHERE status = 'Pending'")
    pending_tasks = cursor.fetchone()[0]

    # Fetch the number of completed tasks
    cursor.execute("SELECT COUNT(*) FROM tasks WHERE status = 'Completed'")
    completed_tasks = cursor.fetchone()[0]
    conn.commit()
    conn.close()
    print("deleted data:", del_count)
    return render_template('new_dashboard.html', appointments=appointments, total_bookings=total_bookings,total_tasks=total_tasks, pending_tasks= pending_tasks ,completed_tasks=completed_tasks,clients=clients ,total_clients=total_clients ,delete=delete, total_deleted_records=total_deleted_records,last_booking_id=last_booking_id,completed_bookings=completed_bookings)

@app.route('/blog_1')
def blog_1():
    return render_template('blog_1.html')
@app.route('/blog_2')
def blog_2():
    return render_template('blog_2.html')
@app.route('/blog_3')
def blog_3():
    return render_template('blog_3.html')

@app.route('/reset_password')
def reset():
    return render_template('reset_password.html')

@app.route('/video_call_2', methods=['GET', 'POST'])
def video_call_2():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # Connect to the database
        conn = sqlite3.connect('lawfirm.db')
        cursor = conn.cursor()

        # Check if the email and password match in the lawyers table
        cursor.execute("SELECT * FROM lawyers WHERE email = ? AND password = ?", (email, password))
        lawyer = cursor.fetchone()
        conn.close()

        if lawyer:
            # Redirect to the create-room page if credentials match
            return redirect(url_for('create_room_2'))
        else:
            # If credentials don't match, show an error message
            flash('Invalid email or password. Please try again.', 'error')
            return render_template('video_call_2.html')

    return render_template('video_call_2.html')

@app.route('/create_room_2', methods=['GET'])
def create_room_2():
    return render_template('create_room_2.html')

@app.route('/join_room', methods=['GET', 'POST'])
def join_room_page():
    if request.method == 'POST':
        room_key = request.form.get('room_key')
        if room_key:
            return redirect(url_for('join_room_page', room=room_key))
        else:
            flash('Please enter a valid room key.', 'error')
    return render_template('join_room.html')

@app.route('/video_call_room')
def video_call_room():
    room_key = request.args.get('room')
    if not room_key:
        flash('Room key is missing.', 'error')
        return redirect(url_for('join_room_page'))
    return render_template('video_call_room.html', room_key=room_key)

@app.route('/payments', methods=['GET'])
def payments():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM qr_payment ORDER BY date DESC, time DESC')
    qr_payment = cursor.fetchall()
    conn.close()
    return render_template('payments.html', qr_payment=qr_payment)

@app.route('/delete_payment/<int:payment_id>', methods=['GET'])
def delete_payment(payment_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM qr_payment WHERE id = ?', (payment_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('payments'))

if __name__ == '__main__': # Initialize the database when the app starts
    app.run(debug=True,port=5001)
    #app.run()
