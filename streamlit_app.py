### streamlit_app.py
import streamlit as st
import pytz
import os
import json
from datetime import datetime, timedelta
from user_settings import load_settings, save_settings
from goal_data_loader import load_goal_data, save_goal_data
from crew_planner import plan_tasks
from whatsapp_utils import send_whatsapp, get_motivational_quote

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

    st.markdown("---")
    st.subheader("🔔 Reminder Preferences")
    reminder_type = st.radio("When would you like WhatsApp reminders?", ["Daily", "Weekly"])
    reminder_time = st.time_input("⏰ Reminder Time", value=datetime.now().time())
    settings["reminder_type"] = reminder_type
    settings["reminder_time"] = reminder_time.strftime("%H:%M")
    save_settings(settings)

# --- Main UI ---
st.title("📆 AI Goal Tracker")
goal = st.text_input("🎯 What's your goal?")
days = st.slider("📅 How many days to complete it?", 1, 30, 5)

if st.button("🚀 Create My Plan"):
    if goal:
        st.info("Planning your journey with AI...")
        tasks = plan_tasks(goal, days)
        for t in tasks:
            t["completed"] = False  # Add completed flag
        save_goal_data({"goal": goal, "days": days, "tasks": tasks})
        st.success("Your plan is ready!")

# --- Load and Display Plan ---
data = load_goal_data()
if data:
    st.header(f"📋 Your Goal: {data['goal']}")
    tz = pytz.timezone(settings.get("timezone", "UTC"))
    today = datetime.now(tz).day

    completed_count = 0
    for i, task in enumerate(data["tasks"]):
        col1, col2 = st.columns([0.1, 0.9])
        with col1:
            checked = st.checkbox("", value=task.get("completed", False), key=f"task_{i}")
        with col2:
            st.markdown(f"**Day {task['day']}:** {task['task']}")
        data["tasks"][i]["completed"] = checked
        if checked:
            completed_count += 1

    save_goal_data(data)

    st.progress(completed_count / len(data["tasks"]))

    # --- Motivation Section ---
    st.markdown("---")
    st.subheader("💡 Daily Motivation")
    st.info(get_motivational_quote())

    # --- WhatsApp Reminder ---
    st.markdown("---")
    if st.button("📤 Send WhatsApp Reminder Now"):
        today_task = next((t for t in data["tasks"] if t["day"] == today), None)
        msg = f"🎯 Goal: {data['goal']}\n"
        if today_task:
            msg += f"📅 Day {today_task['day']}: {today_task['task']}\n"
        msg += f"💡 Motivation: {get_motivational_quote()}"
        try:
            send_whatsapp(msg)
            st.success("Reminder sent!")
        except Exception as e:
            st.error(f"Failed to send reminder: {e}")


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
import random

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

def get_motivational_quote():
    quotes = [
        "Success is the sum of small efforts repeated daily.",
        "Every step forward brings you closer to your goal.",
        "Consistency beats intensity.",
        "You don't have to be great to start, but you have to start to be great.",
        "Progress, not perfection!"
    ]
    return random.choice(quotes)


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
        return {"timezone": "UTC", "reminder_type": "Daily", "reminder_time": "08:00"}

def save_settings(data):
    with open(SETTINGS_FILE, "w") as f:
        json.dump(data, f, indent=2)








    



