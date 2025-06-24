import json
import os

SETTINGS_DIR = "user_settings"

if not os.path.exists(SETTINGS_DIR):
    os.makedirs(SETTINGS_DIR)

def get_settings_file(user_id):
    return os.path.join(SETTINGS_DIR, f"{user_id}.json")

def load_settings(user_id):
    try:
        with open(get_settings_file(user_id), "r") as f:
            return json.load(f)
    except:
        return {"timezone": "UTC", "whatsapp": "", "daily": True, "weekly": False}

def save_settings(user_id, data):
    with open(get_settings_file(user_id), "w") as f:
        json.dump(data, f, indent=2)

def load_all_settings():
    all_settings = {}
    for filename in os.listdir(SETTINGS_DIR):
        if filename.endswith(".json"):
            user_id = filename.replace(".json", "")
            with open(os.path.join(SETTINGS_DIR, filename), "r") as f:
                all_settings[user_id] = json.load(f)
    return all_settings



