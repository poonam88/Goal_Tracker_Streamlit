### streamlit_app.py

import streamlit as st
import pytz
from datetime import datetime
from user_settings import load_settings, save_settings
from goal_data_loader import load_goal_data, save_goal_data
from crew_planner import plan_tasks
from whatsapp_utils import send_whatsapp
import random

# --- Load Settings ---
settings = load_settings()
timezone_list = pytz.all_timezones

# --- Sidebar for Timezone and Reminder Time ---
with st.sidebar:
    st.header("🕒 Time & Reminders")

    selected_timezone = st.selectbox("🌍 Select Timezone", timezone_list, index=timezone_list.index(settings.get("timezone", "UTC")))
    reminder_hour = st.slider("⏰ Reminder Hour (24h format)", 0, 23, settings.get("reminder_hour", 9))

    if selected_timezone != settings.get("timezone") or reminder_hour != settings.get("reminder_hour"):
        settings["timezone"] = selected_timezone
        settings["reminder_hour"] = reminder_hour
        save_settings(settings)
        st.success("✅ Reminder settings updated")

# --- Title ---
st.title("🎯 AI-Powered Goal Tracker")

# --- Input Section ---
goal = st.text_input("What is your goal? (e.g., Learn Python)")
days = st.slider("How many days to achieve it?", 1, 30, 5)

if st.button("✨ Create AI Plan"):
    tasks = plan_tasks(goal, days)
    for task in tasks:
        task["completed"] = False
    save_goal_data({"goal": goal, "tasks": tasks})
    st.success("✅ Plan created successfully!")

# --- Load Data ---
data = load_goal_data()
tasks = data.get("tasks", [])

# --- Show Tasks with Checkboxes ---
if tasks:
    st.subheader(f"📋 Plan for: {data['goal']}")
    completed_count = 0
    for i, task in enumerate(tasks):
        task_key = f"task_{i}"
        checked = st.checkbox(f"Day {task['day']}: {task['task']}", value=task.get("completed", False), key=task_key)
        tasks[i]["completed"] = checked
        if checked:
            completed_count += 1

    save_goal_data(data)

    # --- Progress Bar ---
    progress = completed_count / len(tasks)
    st.progress(progress)

    # --- Motivation ---
    quotes = [
        "Believe in yourself. Every day is a new beginning!",
        "Small steps lead to big changes.",
        "You’re closer than you think. Keep going!",
        "Progress, not perfection.",
        "Your only limit is you."
    ]
    st.info("💡 Motivation: " + random.choice(quotes))

    # --- WhatsApp Reminder Button ---
    if st.button("📤 Send WhatsApp Reminder"):
        now = datetime.now(pytz.timezone(settings.get("timezone", "UTC")))
        today_task = next((t for t in tasks if t["day"] == now.day), None)
        quote = random.choice(quotes)

        if today_task:
            msg = f"📅 Day {today_task['day']} Task: {today_task['task']}\n💡 Motivation: {quote}"
        else:
            msg = f"✅ No scheduled task today.\n💡 Motivation: {quote}"

        try:
            send_whatsapp(msg)
            st.success("✅ WhatsApp reminder sent!")
        except Exception as e:
            st.error(f"❌ Failed to send: {e}")







    



