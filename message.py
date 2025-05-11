import smtplib
from email.mime.text import MIMEText

sender_email = "sidupatnaik216@gmail.com"
receiver_email = "yogendrapatnaik1234@gmail.com"
password = "hdku bjwa szlt qmik"  # App password from Gmail

msg = MIMEText("Test email from Python.")
msg['Subject'] = "Test"
msg['From'] = sender_email
msg['To'] = receiver_email

try:
    server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    server.login(sender_email, password)
    server.send_message(msg)
    server.quit()
    print("Email sent successfully!")
except Exception as e:
    print("Failed to send email:", e)
