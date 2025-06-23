import streamlit as st
from crew_planner import plan_tasks  # Your AI task planner
from whatsapp_utils import send_whatsapp
from user_settings import load_settings, save_settings
import pytz
import os

st.set_page_config(page_title="Goal Tracker AI", page_icon="🚀")

st.title("🚀 Goal Tracker AI")
st.subheader("Turn your big goals into daily tasks with AI coaching")

# Input section
goal = st.text_input("🎯 Enter your goal (e.g., Learn Data Science):")
days = st.number_input("📅 How many days do you want to achieve it?", min_value=1, max_value=30, value=5)

if st.button("Create Plan"):
    if not goal.strip():
        st.warning("Please enter a goal.")
    else:
        with st.spinner("Planning your daily tasks..."):
            task_list = plan_tasks(goal, days)
            if isinstance(task_list, list):
                st.session_state['tasks'] = task_list
                st.session_state['goal'] = goal
                st.session_state['days'] = days
            else:
                st.error("❌ Task generation failed. Please try again.")

# Display results
if 'tasks' in st.session_state:
    st.success(f"📌 Plan for: **{st.session_state['goal']}** in {st.session_state['days']} days")
    for task in st.session_state['tasks']:
        st.markdown(f"**Day {task['day']}**: {task['task']}")


if 'tasks' in st.session_state:
    today = st.session_state['tasks'][0]  # assuming Day 1 for simplicity
    if st.button("📲 Send Today's Task on WhatsApp"):
        msg = f"✅ Your Day {today['day']} Goal: {today['task']}"
        sent = send_whatsapp(msg)
        if sent:
            st.success("WhatsApp reminder sent successfully! ✅")
        else:
            st.error("❌ Failed to send WhatsApp message.")


st.sidebar.title("🔧 Settings")
time_input = st.sidebar.time_input("⏰ Choose daily reminder time", value=None)
if time_input:
    settings = load_settings()
    settings["reminder_time"] = time_input.strftime("%H:%M")
    save_settings(settings)
    st.sidebar.success(f"Reminder time saved: {settings['reminder_time']}")


time_input = st.sidebar.time_input("⏰ Reminder Time", value=None)
timezone_list = pytz.all_timezones
selected_tz = st.sidebar.selectbox("🌐 Timezone", options=timezone_list, index=timezone_list.index("Asia/Kolkata"))

if time_input:
    settings = load_settings()
    settings["reminder_time"] = time_input.strftime("%H:%M")
    settings["timezone"] = selected_tz
    save_settings(settings)
    st.sidebar.success(f"Saved: {settings['reminder_time']} in {settings['timezone']}")

Load existing goal/task data
data = load_goal_data()
settings = load_settings()

# Show goal and tasks
st.title("🎯 Goal Tracker AI")
if "goal" in data and "tasks" in data:
    st.success(f"🎯 Your goal: **{data['goal']}**")

    st.subheader("✅ Today's Task")
    # Timezone logic
    timezone = settings.get("timezone", "UTC")
    user_now = datetime.now(pytz.timezone(timezone))
    today_day = user_now.day

    # Find today's task
    todays_task = next((t for t in data["tasks"] if t["day"] == today_day), None)
    if todays_task:
        st.write(f"📅 Day {todays_task['day']}: {todays_task['task']}")
    else:
        st.warning("No task found for today!")

    # 👉 Add this block for "Next Task Preview" right after today's task
    st.subheader("🔮 Next Task Preview")
    next_task = next((t for t in data["tasks"] if t["day"] == today_day + 1), None)
    if next_task:
        st.info(f"📆 Day {next_task['day']}: {next_task['task']}")
    else:
        st.info("🎉 All tasks completed or no further tasks available.")

