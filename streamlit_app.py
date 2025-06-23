import streamlit as st
import pytz
from datetime import datetime
from user_settings import load_settings, save_settings
from goal_data_loader import load_goal_data
from whatsapp_utils import send_whatsapp

# --- Sidebar ---
with st.sidebar:
    st.header("⚙️ Settings")

    timezone_list = pytz.all_timezones
    current_settings = load_settings()
    selected_timezone = st.selectbox("🌍 Choose your timezone", timezone_list, index=timezone_list.index(current_settings.get("timezone", "UTC")))
    
    if selected_timezone != current_settings.get("timezone"):
        current_settings["timezone"] = selected_timezone
        save_settings(current_settings)
        st.success(f"Timezone updated to {selected_timezone}")
    
    # Toggle for tomorrow’s task
    if "preview" not in st.session_state:
        st.session_state["preview"] = False
    
    st.checkbox("👁️ Show Tomorrow's Task Preview", key="preview")


st.divider()

if st.button("📤 Send Today's Task on WhatsApp"):
    tz = pytz.timezone(current_settings.get("timezone", "UTC"))
    today = datetime.now(tz).day
    data = load_goal_data()
    today_task = next((t for t in data.get("tasks", []) if t["day"] == today), None)

    if today_task:
        msg = f"📅 Day {today_task['day']} Task: {today_task['task']}"
    else:
        msg = "✅ No task for today or you've completed your plan!"

    try:
        send_whatsapp(msg)
        st.success("✅ WhatsApp reminder sent!")
    except Exception as e:
        st.error(f"❌ Failed to send: {e}")


    



