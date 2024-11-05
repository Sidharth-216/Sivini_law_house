# app.py
from flask import Flask, render_template, request, redirect, url_for, session,flash
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
from flask_socketio import SocketIO, emit,join_room
from flask import jsonify,abort
from flask_cors import CORS
#from flask_login import current_user, login_required

app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)
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
    return sqlite3.connect('lawfirm.db', timeout=140)  # Increased timeout

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



@app.route('/about')
def about():
    return render_template('about.html') 


def connect_to_database():
    try:
        conn = sqlite3.connect('lawfirm.db', timeout=140)  # Ensure the path is correct
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


# Route for the video call page
@app.route('/video')
def video_call():
    room = request.args.get('room')
    return render_template('video.html', room=room)

# Socket event for a user joining a room
@socketio.on('join')
def handle_join(data):
    room = data['room']
    join_room(room)
    emit('user-joined', room=room)

# Signaling events for WebRTC within a specific room
@socketio.on('offer')
def handle_offer(data):
    room = data['room']
    emit('offer', data, room=room)

@socketio.on('answer')
def handle_answer(data):
    room = data['room']
    emit('answer', data, room=room)

@socketio.on('ice-candidate')
def handle_ice_candidate(data):
    room = data['room']
    emit('ice-candidate', data, room=room)


# Route to send a new message
@app.route('/send_message', methods=['POST','GET'])
def send_message():
    #data = request.get_json()
    #sender_id = data.get('sender_id')
    #receiver_id = data.get('receiver_id')
    #message_text = data.get('message')

    #if sender_id and receiver_id and message_text:
        #conn = get_db_connection()
        #conn.execute('INSERT INTO messages (sender_id, receiver_id, text, time) VALUES (?, ?, ?, ?)',
                     #(sender_id, receiver_id, message_text, datetime.now()))
        #conn.commit()
        #conn.close()
        #return jsonify({'status': 'success'}), 200
    #else:
        #return jsonify({'status': 'error', 'message': 'Invalid data'}), 400
 return render_template('send_message.html')
    
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

@app.route('/lawyer_login',methods=['GET','POST'])
def lawyer_login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        conn = connect_to_database()  # Ensure this connects to the correct database
        cursor = conn.cursor()
        try:
            # Check if the user exists with the provided username and password
            cursor.execute("SELECT * FROM lawyers WHERE email = ? AND password = ?", (email, password))
            user = cursor.fetchone()

            if user:
                # Store user information in session
                #session['username'] = user[1]  #  username is the first column
                #session['email'] = user[6]      #  email is the sixth column
                #session['number'] = user[7]  # phone number is the seventh column
                #session['profile_picture'] = user[0]  # Assuming profile picture is the zero column
                print("Login successful for user:", email)  # Debugging output
                return redirect(url_for('dashboard'))  # Redirect to profile after login
            else:
                print("Login failed for user:", email)  # Debugging output
                return redirect(url_for('lawyer_register'))
        except Exception as e:
            print(f"An error occurred during login: {e}")  # Log the exact error for debugging
            return f"An error occurred during login: {e}"  # Return the error message
        finally:
            cursor.close()
            conn.close()

    return render_template('lawyer_login.html')

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
    conn = get_db_connection()
    conn.execute('DELETE FROM bookings WHERE id = ?', (appointment_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('appointment_management'))  # Redirect to appointment management page

def get_db_connection():
    conn = sqlite3.connect('lawfirm.db')  # Path to your database
    conn.row_factory = sqlite3.Row  # Allow access to columns by name
    return conn

# Route to fetch messages for the lawyer dashboard
@app.route('/message_management', methods=['GET'])
def message_management():
    # This route will render the message management interface for the lawyer
    return render_template('message_management.html')  # Adjust this to your actual template file

# Route to fetch messages
@app.route('/messages', methods=['GET'])
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
    return jsonify(messages_list)

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
def load_user(user_id):
    # Load the user from the database
    return User.get(user_id)  # Adjust this based on your user model

@app.route('/upload_document', methods=['POST'])
def upload_document():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)

    file = request.files['file']
    client_name = request.form['client_name']  # Get the client name from form

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(file_path)

        conn = get_db_connection()
        conn.execute('INSERT INTO documents (lawyer_id, client_name, document_name, document_path) VALUES (?, ?, ?, ?)',
                     (current_user.id, client_name, filename, file_path))
        conn.commit()
        conn.close()

        flash('Document uploaded successfully!')
        return redirect(url_for('document_management'))

    flash('Invalid file type. Allowed types are: pdf, doc, docx, jpg, png.')
    return redirect(request.url)

@app.route('/document_management', methods=['GET', 'POST'])
#@login_required  # Ensures only logged-in users can access this route
def document_management():
    #if request.method == 'POST':
        #client_name = request.form['client_name']
        #file = request.files['file']
        # Save the file and client_name to your database
    
    #documents = fetch_documents()  # Replace with your fetch logic
    
    # Now, render the template, ensuring the user is logged in
    return render_template('document_management')

@app.route('/delete_document/<int:document_id>', methods=['POST'])
def delete_document(document_id):
    #conn = get_db_connection()
    #document = conn.execute('SELECT * FROM documents WHERE id = ?', (document_id,)).fetchone()
    #if document:
        #os.remove(document['document_path'])  # Delete the file from the server
        #conn.execute('DELETE FROM documents WHERE id = ?', (document_id,))
        #conn.commit()
    #conn.close()
    #flash('Document deleted successfully!')
    return redirect(url_for('document_management'))

@app.route('/notifications', methods=['GET', 'POST'])
def notifications():
    return render_template('notifications.html')

@app.route('/delete_notification/<int:notification_id>', methods=['POST'])
def delete_notification(notification_id):
    conn = sqlite3.connect('lawfirm.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM notifications WHERE id = ?", (notification_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('notifications'))

if __name__ == '__main__': # Initialize the database when the app starts
    app.run(debug=True,port=5001)
    #app.run()