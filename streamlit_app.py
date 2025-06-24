import streamlit as st
import pytz
import random
from datetime import datetime
from user_settings import load_settings, save_settings
from goal_data_loader import load_goal_data, save_goal_data
from crew_planner import plan_tasks
from whatsapp_utils import send_whatsapp

# --- Motivational Quotes ---
MOTIVATION_QUOTES = [
    "You're one step closer to your goal. Keep going!",
    "Progress, not perfection.",
    "Small steps every day lead to big changes.",
    "Your future self will thank you.",
    "Success is built on consistency, not intensity.",
    "Every day is a fresh chance to move ahead!"
]

# --- Sidebar ---
with st.sidebar:
    st.header("⚙️ Settings")

    timezone_list = pytz.all_timezones
    settings = load_settings()
    selected_timezone = st.selectbox("🌍 Choose your timezone", timezone_list, 
                                     index=timezone_list.index(settings.get("timezone", "UTC")))
    if selected_timezone != settings.get("timezone"):
        settings["timezone"] = selected_timezone
        save_settings(settings)
        st.success(f"Timezone updated to {selected_timezone}")

    # WhatsApp preference
    send_mode = st.radio("📲 WhatsApp Reminder Mode", ["Daily Motivation", "Weekly Summary"])
    settings["send_mode"] = send_mode
    save_settings(settings)

# --- Main App ---
st.title("🎯 Turn your big goals into daily tasks")

goal = st.text_input("🎯 Enter your goal (e.g., Learn Data Science):")
days = st.slider("📅 How many days do you want to achieve it?", 1, 30, 5)

if st.button("🚀 Create Plan"):
    if goal:
        st.info("🧠 Planning your journey using AI...")
        tasks = plan_tasks(goal, days)
        save_goal_data({"goal": goal, "days": days, "tasks": tasks})
        st.success(f"📌 Plan for: **{goal}** in {days} days")
        for task in tasks:
            st.markdown(f"**Day {task['day']}:** {task['task']}")

# --- Load & Display Task Checklist ---
data = load_goal_data()
settings = load_settings()
tz = pytz.timezone(settings.get("timezone", "UTC"))
today = datetime.now(tz).day

if data:
    st.markdown("## ✅ Task Checklist")
    if "checked_tasks" not in st.session_state:
        st.session_state.checked_tasks = []

    for task in data.get("tasks", []):
        label = f"Day {task['day']}: {task['task']}"
        key = f"task_{task['day']}"
        checked = st.checkbox(label, key=key)
        if checked and task["day"] not in st.session_state.checked_tasks:
            st.session_state.checked_tasks.append(task["day"])
        elif not checked and task["day"] in st.session_state.checked_tasks:
            st.session_state.checked_tasks.remove(task["day"])

    if st.session_state.checked_tasks:
        st.markdown("## 📋 Tasks Scheduled for Today")
        for day in st.session_state.checked_tasks:
            task = next((t for t in data["tasks"] if t["day"] == day), None)
            if task:
                st.info(f"✔️ Day {task['day']}: {task['task']}")

# --- Send WhatsApp Reminder Automatically (Optional Manual Trigger for testing)
if st.button("📤 Test WhatsApp Reminder"):
    today_task = next((t for t in data.get("tasks", []) if t["day"] == today), None)
    if today_task:
        quote = random.choice(MOTIVATION_QUOTES)
        msg = f"📅 Day {today_task['day']} Task:\n{today_task['task']}\n\n💡 Motivation: {quote}"
    else:
        msg = "✅ No task for today or you've completed your plan!"

    try:
        send_whatsapp(msg)
        st.success("✅ WhatsApp reminder sent!")
    except Exception as e:
        st.error(f"❌ Failed to send: {e}")







    



