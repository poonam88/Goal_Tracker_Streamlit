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

    reminder_type = settings.get("reminder_type", "daily")

    if reminder_type == "daily":
        task = next((t for t in data.get("tasks", []) if t["day"] == today), None)
        if task:
            msg = f"📅 Day {task['day']} Task: {task['task']}\n💡 Stay motivated! You've got this! 💪"
        else:
            msg = "✅ All tasks completed or no task for today!"
    else:  # weekly
        this_week = [t for t in data.get("tasks", []) if today <= t["day"] < today + 7]
        if this_week:
            msg = "📊 **Your Weekly Plan:**\n" + "\n".join(
                [f"• Day {t['day']}: {t['task']}" for t in this_week])
        else:
            msg = "🎉 No upcoming tasks this week. Enjoy your free time!"

    try:
        send_whatsapp(msg)
        print("✅ WhatsApp reminder sent!")
    except Exception as e:
        print(f"❌ Failed to send: {e}")
