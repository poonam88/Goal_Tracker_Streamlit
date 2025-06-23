# scheduled_task_sender.py
import pytz
from datetime import datetime
from goal_data_loader import load_goal_data
from user_settings import load_settings
from whatsapp_utils import send_whatsapp

def send_daily_task():
    settings = load_settings()
    data = load_goal_data()
    tz = pytz.timezone(settings.get("timezone", "UTC"))
    today = datetime.now(tz).day

    today_task = next((t for t in data.get("tasks", []) if t["day"] == today), None)
    if today_task:
        msg = f"📅 Day {today_task['day']} Task: {today_task['task']}"
    else:
        msg = "✅ No task for today or you've completed your plan!"

    try:
        send_whatsapp(msg)
        print("✅ WhatsApp sent automatically")
    except Exception as e:
        print(f"❌ Failed: {e}")
