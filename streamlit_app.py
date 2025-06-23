import streamlit as st
from datetime import datetime
import pytz
import json
import os

from goal_data_loader import load_goal_data, save_goal_data
from user_settings import load_settings, save_settings
from crew_planner import plan_tasks
from whatsapp_utils import send_whatsapp

st.set_page_config(page_title="Goal Tracker AI", layout="centered")

st.title("🎯 Goal Tracker AI")
st.caption("Powered by CrewAI + Streamlit + Twilio")

# --- Sidebar: Settings ---
with st.sidebar:
    st.header("⚙️ Settings")

    # Timezone Selector
    all_timezones = pytz.all_timezones
    settings = load_settings()
    selected_tz = st.selectbox("🌍 Choose Timezone", all_timezones,
                               index=all_timezones.index(settings.get("timezone", "UTC")))
    settings["timezone"] = selected_tz
    save_settings(settings)

    # Tomorrow Task Preview Toggle
    if "preview" not in st.session_state:
        st.session_state["preview"] = False
    st.session_state["preview"] = st.checkbox("👁️ Show Tomorrow's Task Preview")

    st.divider()

    # Manual WhatsApp Trigger
    if st.button("📤 Send WhatsApp Reminder Now"):
        data = load_goal_data()
        tz = pytz.timezone(settings["timezone"])
        today = datetime.now(tz).day
        today_task = next((t for t in data.get("tasks", []) if t["day"] == today), None)
        if today_task:
            msg = f"📅 Day {today_task['day']} Task: {today_task['task']}"
        else:
            msg = "✅ All tasks completed or no task found for today!"
        try:
            send_whatsapp(msg)
            st.success("✅ WhatsApp reminder sent!")
        except Exception as e:
            st.error(f"❌ Failed to send: {e}")

# --- Main Section ---
st.subheader("📝 Set Your Learning Goal")
goal = st.text_input("What would you like to learn or achieve?", key="goal_input")

days = st.slider("📆 Duration (Days)", min_value=1, max_value=30, value=5)

if st.button("🚀 Generate Plan"):
    if goal:
        st.info("🧠 AI planning your daily learning journey...")
        task_list = plan_tasks(goal, days)
        save_goal_data({
            "goal": goal,
            "days": days,
            "tasks": task_list
        })
        st.success("✅ Plan generated successfully!")

# --- Show Today's Task ---
data = load_goal_data()
if data:
    st.markdown("## 📌 Today's Task")
    tz = pytz.timezone(settings.get("timezone", "UTC"))
    today = datetime.now(tz).day
    today_task = next((t for t in data["tasks"] if t["day"] == today), None)
    if today_task:
        st.success(f"Day {today_task['day']}: {today_task['task']}")
    else:
        st.info("🎉 No task for today or you've completed your plan!")

# --- Tomorrow Preview ---
if st.session_state["preview"]:
    st.markdown("## 🔮 Tomorrow's Task Preview")
    tomorrow_task = next((t for t in data["tasks"] if t["day"] == today + 1), None)
    if tomorrow_task:
        st.info(f"📅 Day {tomorrow_task['day']}: {tomorrow_task['task']}")
    else:
        st.warning("🥳 No task scheduled for tomorrow!")

    



