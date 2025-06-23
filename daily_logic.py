import os
from whatsapp_utils import send_whatsapp
from goal_data_loader import load_goal_data, save_goal_data

def run_daily_reminder():
    data = load_goal_data()
    current_day = data.get("current_day", 1)
    tasks = data.get("tasks", [])
    goal = data.get("goal", "your goal")
    days = data.get("days", len(tasks))

    if current_day <= len(tasks):
        today_task = tasks[current_day - 1]
        message = f"📌 Goal: {goal}\n🗓️ Day {current_day} of {days}\n🧠 Today's Task: {today_task}"
        send_whatsapp(os.getenv("USER_WHATSAPP"), message)
        data["current_day"] = current_day + 1
        save_goal_data(data)