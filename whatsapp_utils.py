from twilio.rest import Client
import os

def send_whatsapp(to_number, message):
    client = Client(os.getenv("TWILIO_SID"), os.getenv("TWILIO_AUTH_TOKEN"))
    from_number = "whatsapp:+14155238886"  # Twilio Sandbox number
    client.messages.create(
        body=message,
        from_=from_number,
        to=to_number
    )