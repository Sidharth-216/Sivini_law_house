import sqlite3
import shutil
import os
from datetime import datetime
import smtplib
from email.message import EmailMessage

# === CONFIGURATION ===
DB_PATH = "lawfirm.db"
BACKUP_DIR = "db_backups"
LOG_FILE = "maintenance_log.txt"

# Optional Email Settings (set these if you want email notifications)
EMAIL_ENABLED = False  # Set to True to enable email alerts
EMAIL_SENDER = "youremail@example.com"
EMAIL_RECEIVER = "youremail@example.com"
EMAIL_PASSWORD = "your_email_password"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

# === FUNCTION TO APPEND TO LOG ===
def log(message):
    timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    full_msg = f"{timestamp} {message}"
    print(full_msg)
    with open(LOG_FILE, "a") as f:
        f.write(full_msg + "\n")

# === BACKUP DATABASE ===
def backup_database():
    os.makedirs(BACKUP_DIR, exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    backup_path = os.path.join(BACKUP_DIR, f"lawfirm_backup_{timestamp}.db")
    shutil.copy(DB_PATH, backup_path)
    log(f"Backup created: {backup_path}")

# === VACUUM DATABASE ===
def vacuum_database():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("VACUUM;")
        log("VACUUM completed.")

# === ANALYZE DATABASE ===
def analyze_database():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("ANALYZE;")
        log("ANALYZE completed.")

# === INTEGRITY CHECK ===
def integrity_check():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.execute("PRAGMA integrity_check;")
        result = cursor.fetchone()[0]
        if result == "ok":
            log("Integrity check passed.")
        else:
            log("Integrity check failed!")
            log(result)

# === EMAIL NOTIFICATION ===
def send_email_log():
    if not EMAIL_ENABLED:
        return
    with open(LOG_FILE, "r") as f:
        log_content = f.read()

    msg = EmailMessage()
    msg.set_content(log_content)
    msg["Subject"] = "SQLite Maintenance Report"
    msg["From"] = EMAIL_SENDER
    msg["To"] = EMAIL_RECEIVER

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.send_message(msg)
            log("Email sent successfully.")
    except Exception as e:
        log(f"Email failed: {e}")

# === MAIN ===
if __name__ == "__main__":
    log("=== SQLite Maintenance Started ===")
    backup_database()
    vacuum_database()
    analyze_database()
    integrity_check()
    send_email_log()
    log("=== SQLite Maintenance Complete ===")
