from datetime import datetime, timedelta
import pytz

def get_utc_cron_from_local(reminder_time, timezone):
    hour, minute = map(int, reminder_time.split(":"))
    local_tz = pytz.timezone(timezone)
    
    local_time = local_tz.localize(datetime(2024, 1, 1, hour, minute))
    utc_time = local_time.astimezone(pytz.utc)

    return f"{utc_time.minute} {utc_time.hour} * * *"  # for Streamlit scheduler
