import pytz
import os
import random
from datetime import datetime
from goal_data_loader import load_goal_data
from user_settings import load_settings
from whatsapp_utils import send_whatsapp

MOTIVATION_QUOTES = [
    "You're one step closer to your goal. Keep going!",
    "Progress, not perfection.",
    "Small steps every day lead to big changes.",
    "Your future self will thank you.",
    "Success is built on consistency, not intensity.",
    "Every day is a fresh chance to move ahead!"
]

def send_daily_whatsapp_reminder():
    try:
        settings = load_settings()
        tz = pytz.timezone(settings.get("timezone", "UTC"))
        today = datetime.now(tz).day

        data = load_goal_data()
        today_task = next((t for t in data.get("tasks", []) if t["day"] == today), None)

        if today_task:
            quote = random.choice(MOTIVATION_QUOTES)
            msg = f"📅 Day {today_task['day']} Task:\n{today_task['task']}\n\n💡 Motivation: {quote}"
        else:
            msg = "✅ No task for today or you've completed your plan!"

        send_whatsapp(msg)
        print("✅ WhatsApp reminder sent successfully!")

    except Exception as e:
        print(f"❌ Failed to send WhatsApp message: {e}")


if __name__ == "__main__":
    send_daily_whatsapp_reminder()
