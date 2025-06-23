from twilio.rest import Client
import os

def send_whatsapp(message: str):
    account_sid = os.getenv("TWILIO_SID")
    auth_token = os.getenv("TWILIO_AUTH_TOKEN")
    from_whatsapp = os.getenv("TWILIO_PHONE")
    to_whatsapp = os.getenv("USER_WHATSAPP")

    client = Client(account_sid, auth_token)

    try:
        message = client.messages.create(
            body=message,
            from_=from_whatsapp,
            to=to_whatsapp
        )
        return True
    except Exception as e:
        print("❌ Failed to send message:", e)
        return False
