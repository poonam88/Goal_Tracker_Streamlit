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


    



