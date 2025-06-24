### streamlit_app.py
import streamlit as st
import pytz
from datetime import datetime
from user_settings import load_settings, save_settings
from goal_data_loader import load_all_users_data, save_user_data
from crew_planner import plan_tasks
from whatsapp_utils import send_whatsapp
import uuid

# --- Identify User ---
if "user_id" not in st.session_state:
    st.session_state.user_id = str(uuid.uuid4())  # generate unique ID per session
user_id = st.session_state.user_id

# --- Sidebar ---
with st.sidebar:
    st.header("⚙️ Settings")
    timezone_list = pytz.all_timezones
    settings = load_settings(user_id)
    selected_timezone = st.selectbox("🌍 Choose your timezone", timezone_list, 
                                     index=timezone_list.index(settings.get("timezone", "UTC")))
    
    user_whatsapp = st.text_input("📱 Your WhatsApp Number (with country code)", value=settings.get("whatsapp", ""))

    schedule_type = st.radio("📬 Reminder Type", ["Daily", "Weekly"])

    if selected_timezone != settings.get("timezone") or user_whatsapp != settings.get("whatsapp") or schedule_type != settings.get("schedule", "Daily"):
        settings["timezone"] = selected_timezone
        settings["whatsapp"] = user_whatsapp
        settings["schedule"] = schedule_type
        save_settings(user_id, settings)
        st.success("✅ Settings updated")

# --- Main UI ---
st.title("🎯 Goal Tracker AI")
goal = st.text_input("🎯 Enter your goal (e.g., Learn Data Science):")
days = st.slider("📅 How many days to complete it?", 1, 30, 5)

if st.button("🚀 Create My Plan"):
    if goal:
        st.info("🧠 Generating your personalized learning plan...")
        tasks = plan_tasks(goal, days)
        save_user_data(user_id, {
            "goal": goal,
            "days": days,
            "tasks": tasks,
            "created": str(datetime.utcnow())
        })
        st.success(f"Plan for: {goal} ({days} days)")

# --- Load Tasks ---
data = load_all_users_data().get(user_id, {})
tasks = data.get("tasks", [])
settings = load_settings(user_id)
timezone = settings.get("timezone", "UTC")

# --- Task Checklist ---
st.markdown("## ✅ Your Progress")
completed = st.session_state.get("completed", set())
progress = 0

for task in tasks:
    checked = st.checkbox(f"Day {task['day']}: {task['task']}", key=f"chk_{task['day']}")
    if checked:
        completed.add(task['day'])
progress = len(completed) / len(tasks) if tasks else 0

st.progress(progress)

# --- Motivation ---
if tasks:
    st.markdown("## 💡 Daily Motivation")
    st.info("Believe in yourself. You are capable of amazing things!")


### scheduler.py
import json
import os
import pytz
from datetime import datetime
from goal_data_loader import load_all_users_data
from user_settings import load_all_settings
from whatsapp_utils import send_whatsapp
from motivation_quotes import get_motivation

all_users = load_all_users_data()
all_settings = load_all_settings()

for user_id, data in all_users.items():
    settings = all_settings.get(user_id, {})
    tz = pytz.timezone(settings.get("timezone", "UTC"))
    now = datetime.now(tz)
    schedule_type = settings.get("schedule", "Daily")
    
    if schedule_type == "Weekly" and now.weekday() != 0:
        continue  # only send on Mondays for weekly

    today = now.day
    tasks = data.get("tasks", [])
    today_task = next((t for t in tasks if t["day"] == today), None)
    if today_task:
        message = f"📅 Day {today_task['day']}: {today_task['task']}\n💡 {get_motivation()}"
    else:
        message = f"✅ No task for today!\n💡 {get_motivation()}"

    to = settings.get("whatsapp")
    if to:
        try:
            send_whatsapp(message, to)
            print(f"Sent to {to}")
        except Exception as e:
            print(f"❌ Failed for {to}: {e}")









    



