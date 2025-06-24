import os
import pytz
import schedule
import time
from datetime import datetime
from goal_data_loader import load_goal_data
from user_settings import load_settings
from whatsapp_utils import send_whatsapp
import random

# Optional motivational quotes list
quotes = [
    "🌟 Keep going, you're doing great!",
    "🚀 One step at a time leads to big goals!",
    "🔥 Stay focused and never give up!",
    "💪 You’ve got this! Today is your day!",
    "🌱 Growth happens daily — keep pushing!"
]

def send_daily_reminder():
    settings = load_settings()
    data = load_goal_data()

    if not data or "tasks" not in data:
        print("No tasks found to send.")
        return

    timezone = settings.get("timezone", "UTC")
    tz = pytz.timezone(timezone)
    today = datetime.now(tz).day

    today_task = next((t for t in data["tasks"] if t["day"] == today), None)

    if today_task:
        quote = random.choice(quotes)
        msg = f"📅 Day {today_task['day']} Task: {today_task['task']}\n\n💡 Motivation: {quote}"
    else:
        msg = "✅ You've completed all tasks or no task found for today!"

    try:
        send_whatsapp(msg)
        print("✅ WhatsApp reminder sent!")
    except Exception as e:
        print(f"❌ Failed to send WhatsApp message: {e}")

def schedule_daily_reminder():
    settings = load_settings()
    reminder_time = settings.get("reminder_time", "08:00")  # default 8 AM
    hour, minute = map(int, reminder_time.split(":"))

    # Schedule it for the system's local time (assumes the server is in UTC or timezone-aware)
    schedule.every().day.at(f"{hour:02d}:{minute:02d}").do(send_daily_reminder)
    print(f"📆 Scheduled reminder daily at {reminder_time} (local server time)")

    while True:
        schedule.run_pending()
        time.sleep(30)

if __name__ == "__main__":
    schedule_daily_reminder()

