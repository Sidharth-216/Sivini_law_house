import sqlite3

def connect_to_database(db_name='lawfirm.db'):
    ...
    try:
        # Establish a connection to the database
        connection = sqlite3.connect('lawfirm.db')
        print("Database connection successful.")
        return connection
    except Exception as e:
        print(f"Error connecting to database: {e}")
        return None
connect_to_database()