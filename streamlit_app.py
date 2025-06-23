import streamlit as st
import pytz
from datetime import datetime
from user_settings import load_settings, save_settings
from goal_data_loader import load_goal_data, save_goal_data
from crew_planner import plan_tasks
from whatsapp_utils import send_whatsapp

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

    if "preview" not in st.session_state:
        st.session_state["preview"] = False

    st.checkbox("👁️ Show Tomorrow's Task Preview", key="preview")

# --- Main UI ---
st.title("🎯 Turn your big goals into daily tasks with AI coaching")

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

# --- Today's Task ---
data = load_goal_data()
tz = pytz.timezone(settings.get("timezone", "UTC"))
today = datetime.now(tz).day

if data:
    st.markdown("## 📅 Today's Task")
    today_task = next((t for t in data["tasks"] if t["day"] == today), None)
    if today_task:
        st.success(f"**Day {today_task['day']}:** {today_task['task']}")
    else:
        st.info("🎉 No task today or you've completed the goal!")

# --- Tomorrow's Preview ---
if st.session_state["preview"]:
    st.markdown("## 🔮 Tomorrow's Task Preview")
    tomorrow_task = next((t for t in data["tasks"] if t["day"] == today + 1), None)
    if tomorrow_task:
        st.info(f"📅 Day {tomorrow_task['day']}: {tomorrow_task['task']}")
    else:
        st.warning("🥳 No task scheduled for tomorrow!")

# --- WhatsApp Reminder ---
st.divider()
if st.button("📤 Send Today's Task on WhatsApp"):
    if today_task:
        msg = f"📅 Day {today_task['day']} Task: {today_task['task']}"
    else:
        msg = "✅ No task for today or you've completed your plan!"
    try:
        send_whatsapp(msg)
        st.success("✅ WhatsApp reminder sent!")
    except Exception as e:
        st.error(f"❌ Failed to send: {e}")



    



