import json
import os

DATA_DIR = "user_data"

if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

def get_user_filename(phone):
    return os.path.join(DATA_DIR, f"{phone}.json")

def load_user_data(phone):
    try:
        with open(get_user_filename(phone), "r") as f:
            return json.load(f)
    except:
        return {"goal": "", "days": 0, "tasks": []}

def save_user_data(phone, data):
    with open(get_user_filename(phone), "w") as f:
        json.dump(data, f, indent=2)

def load_all_users_data():
    users = []
    for filename in os.listdir(DATA_DIR):
        if filename.endswith(".json"):
            with open(os.path.join(DATA_DIR, filename), "r") as f:
                data = json.load(f)
                users.append((filename.replace(".json", ""), data))
    return users
