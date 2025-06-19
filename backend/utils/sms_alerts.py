from twilio.rest import Client
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

TWILIO_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")

def send_sms_alert(phone_number, alert_message):
    """Sends an SMS alert using Twilio."""

    # ✅ Ensure phone number is in correct format
    if phone_number.startswith("0"):
        phone_number = "+91" + phone_number[1:]
    elif not phone_number.startswith("+"):
        phone_number = "+91" + phone_number  # Add country code if missing

    print(f"📲 Sending SMS to {phone_number}...")

    try:
        client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)
        message = client.messages.create(
            body=alert_message,
            from_=TWILIO_PHONE_NUMBER,
            to=phone_number
        )
        print(f"✅ SMS Sent! Message SID: {message.sid}")
        return True
    except Exception as e:
        print(f"⚠️ Error sending SMS: {e}")
        return False
