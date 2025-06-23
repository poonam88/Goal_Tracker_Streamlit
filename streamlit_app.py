import streamlit as st
from datetime import datetime
import pytz
from goal_data_loader import load_goal_data
from crew_planner import plan_tasks
from whatsapp_utils import send_whatsapp
from user_settings import load_settings, save_settings

# Initial setup
st.set_page_config(page_title="🎯 Goal Tracker AI", layout="centered")

# Sidebar
with st.sidebar:
    st.header("⚙️ Settings")

    # Timezone selector
    timezone = st.selectbox("🌍 Choose Your Timezone", pytz.all_timezones, index=pytz.all_timezones.index("Asia/Kolkata"))

    # Save timezone
    save_settings({"timezone": timezone})

    # Preview toggle
    if "preview" not in st.session_state:
        st.session_state["preview"] = False

    st.session_state["preview"] = st.checkbox("👁️ Show Tomorrow's Task Preview")

    st.divider()

    # WhatsApp trigger
    if st.button("📤 Send WhatsApp Reminder Now"):
        data = load_goal_data()
        today = datetime.now(pytz.timezone(timezone)).day
        task_today = next((t for t in data.get("tasks", []) if t["day"] == today), None)
        if task_today:
            message = f"📅 Day {task_today['day']} Task: {task_today['task']}"
        else:
            message = "✅ All tasks completed or not found for today!"
        try:
            send_whatsapp(message)
            st.success("✅ Reminder sent successfully!")
        except Exception as e:
            st.error(f"Failed to send WhatsApp: {e}")

# Main App
st.title("🚀 AI Goal Tracker")

# Goal input
goal = st.text_input("🎯 What is your goal?", "Learn Data Science")
days = st.slider("📆 How many days to complete it?", min_value=3, max_value=30, value=5)

# Plan generator
if st.button("🛠️ Generate Plan"):
    tasks = plan_tasks(goal, days)
    save_data = {"goal": goal, "days": days, "tasks": tasks}
    with open("goal_data.json", "w") as f:
        import json
        json.dump(save_data, f, indent=2)
    st.success("✅ Plan created!")

# Load and show today's task
data = load_goal_data()
timezone = load_settings().get("timezone", "UTC")
user_now = datetime.now(pytz.timezone(timezone))
today_day = user_now.day

st.subheader("📌 Today's Task")
today_task = next((t for t in data.get("tasks", []) if t["day"] == today_day), None)
if today_task:
    st.success(f"📅 Day {today_task['day']}: {today_task['task']}")
else:
    st.warning("No task found for today.")

# Preview tomorrow's task
if st.session_state.get("preview"):
    next_task = next((t for t in data["tasks"] if t["day"] == today_day + 1), None)
    st.subheader("🔮 Tomorrow's Task Preview")
    if next_task:
        st.info(f"📆 Day {next_task['day']}: {next_task['task']}")
    else:
        st.warning("🎉 No tasks remaining or tomorrow's task not found.")


