### streamlit_app.py
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


### crew_planner.py
import os
import json
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def plan_tasks(goal, days):
    prompt = f"""
    Break down the goal \"{goal}\" into {days} daily learning tasks.
    Format the output as JSON like this:
    [
      {{ "day": 1, "task": "..." }},
      {{ "day": 2, "task": "..." }}
    ]
    """
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.6,
    )
    reply = response.choices[0].message.content
    try:
        return json.loads(reply)
    except:
        return [{"day": 1, "task": "Sorry, task breakdown failed!"}]


### whatsapp_utils.py
import os
from twilio.rest import Client

def send_whatsapp(message):
    account_sid = os.getenv("TWILIO_SID")
    auth_token = os.getenv("TWILIO_AUTH_TOKEN")
    from_whatsapp = "whatsapp:+14155238886"
    to_whatsapp = os.getenv("USER_WHATSAPP")

    client = Client(account_sid, auth_token)
    client.messages.create(
        body=message,
        from_=from_whatsapp,
        to=to_whatsapp
    )


### goal_data_loader.py
import json

def save_goal_data(data):
    with open("goal_data.json", "w") as f:
        json.dump(data, f, indent=2)

def load_goal_data():
    try:
        with open("goal_data.json", "r") as f:
            return json.load(f)
    except:
        return {}


### user_settings.py
import json

SETTINGS_FILE = "user_settings.json"

def load_settings():
    try:
        with open(SETTINGS_FILE, "r") as f:
            return json.load(f)
    except:
        return {"timezone": "UTC"}

def save_settings(data):
    with open(SETTINGS_FILE, "w") as f:
        json.dump(data, f, indent=2)




    



