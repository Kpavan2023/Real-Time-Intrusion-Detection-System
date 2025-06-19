import smtplib
import ssl
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

load_dotenv()

EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

def send_email_alert(recipient_email, message):
    print("📩 Attempting to send OTP to:", recipient_email)

    if not EMAIL_USER or not EMAIL_PASSWORD:
        print("❌ EMAIL_USER or EMAIL_PASSWORD not found in environment!")
        return False

    try:
        msg = MIMEMultipart()
        msg["From"] = EMAIL_USER
        msg["To"] = recipient_email
        msg["Subject"] = "Intrusion Detection System"
        msg.attach(MIMEText(message, "plain"))

        context = ssl.create_default_context()
        with smtplib.SMTP(EMAIL_HOST, EMAIL_PORT) as server:
            server.ehlo()
            server.starttls(context=context)
            server.ehlo()
            server.login(EMAIL_USER, EMAIL_PASSWORD)
            server.sendmail(EMAIL_USER, recipient_email, msg.as_string())

        print("✅ Email sent successfully!")
        return True

    except smtplib.SMTPAuthenticationError as e:
        print("❌ SMTP Auth Error: Check Gmail App Password!")
        print(f"Details: {e}")
    except Exception as e:
        print(f"❌ General Error: {e}")

    return False
