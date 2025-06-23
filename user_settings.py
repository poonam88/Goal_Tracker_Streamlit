# user_settings.py

import json

SETTINGS_FILE = "user_settings.json"

def load_settings():
    try:
        with open(SETTINGS_FILE, "r") as f:
            return json.load(f)
    except:
        return {"timezone": "UTC", "reminder_type": "daily"}

def save_settings(data):
    with open(SETTINGS_FILE, "w") as f:
        json.dump(data, f, indent=2)



