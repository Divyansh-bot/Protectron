import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def trigger_alert(message, email_recipient="admin@example.com"):
    """
    Sends a security alert via email and logs the message.
    """

    # Log the alert
    print(f"🚨 ALERT: {message}")

    # Email Configuration (Replace with real credentials)
    SMTP_SERVER = "smtp.example.com"
    SMTP_PORT = 587
    SMTP_USER = "your_email@example.com"
    SMTP_PASS = "your_password"

    sender_email = SMTP_USER
    receiver_email = email_recipient
    subject = "⚠️ Protectron Security Alert"
    
    # Email content
    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg["Subject"] = subject
    msg.attach(MIMEText(message, "plain"))

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASS)
            server.sendmail(sender_email, receiver_email, msg.as_string())

        print("📧 Email Alert Sent!")
    except Exception as e:
        print(f"❌ Email Alert Failed: {e}")

