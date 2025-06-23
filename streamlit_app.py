import streamlit as st
import pytz
from datetime import datetime
from user_settings import load_settings, save_settings
from goal_data_loader import load_goal_data, save_goal_data
from crew_planner import plan_tasks
from whatsapp_utils import send_whatsapp

# --- Sidebar Settings ---
with st.sidebar:
    st.header("⚙️ Settings")

    # Load timezone from settings
    all_timezones = pytz.all_timezones
    settings = load_settings()
    selected_tz = st.selectbox("🌍 Select Your Timezone", all_timezones,
                               index=all_timezones.index(settings.get("timezone", "UTC")))
    settings["timezone"] = selected_tz
    save_settings(settings)

    # Toggle preview
    if "preview" not in st.session_state:
        st.session_state["preview"] = False
    st.session_state["preview"] = st.checkbox("👁️ Show Tomorrow's Task Preview")

    st.divider()

    # Manual WhatsApp reminder
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
st.title("🎯 Turn your big goals into daily tasks with AI coaching")

goal = st.text_input("🎯 Enter your goal (e.g., Learn Data Science):")
days = st.slider("📅 How many days do you want to achieve it?", 1, 30, 5)

if st.button("🚀 Create Plan"):
    if goal:
        st.info("🧠 Planning your journey using AI...")
        task_list = plan_tasks(goal, days)
        save_goal_data({
            "goal": goal,
            "days": days,
            "tasks": task_list
        })
        st.success(f"📌 Plan for: **{goal}** in **{days} days**")
        for task in task_list:
            st.markdown(f"**Day {task['day']}**: {task['task']}")

# --- Show Today's Task ---
data = load_goal_data()
if data:
    st.subheader("📅 Today's Task")
    tz = pytz.timezone(settings.get("timezone", "UTC"))
    today = datetime.now(tz).day
    today_task = next((t for t in data.get("tasks", []) if t["day"] == today), None)
    if today_task:
        st.success(f"**Day {today_task['day']}**: {today_task['task']}")
    else:
        st.info("🎉 No task today or you've completed the goal!")

# --- Show Tomorrow's Task ---
if st.session_state["preview"]:
    st.subheader("🔮 Tomorrow's Task Preview")
    tomorrow_task = next((t for t in data.get("tasks", []) if t["day"] == today + 1), None)
    if tomorrow_task:
        st.info(f"📆 Day {tomorrow_task['day']}: {tomorrow_task['task']}")
    else:
        st.warning("🥳 No task scheduled for tomorrow!")

    



