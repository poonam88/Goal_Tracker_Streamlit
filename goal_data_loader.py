import json
import os

DATA_DIR = "user_data"

if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

def get_user_file(user_id):
    return os.path.join(DATA_DIR, f"{user_id}.json")

def save_user_data(user_id, data):
    with open(get_user_file(user_id), "w") as f:
        json.dump(data, f, indent=2)

def load_user_data(user_id):
    try:
        with open(get_user_file(user_id), "r") as f:
            return json.load(f)
    except:
        return {}

def load_all_users_data():
    all_data = {}
    try:
        for filename in os.listdir(DATA_DIR):
            if filename.endswith(".json"):
                user_id = filename.replace(".json", "")
                with open(os.path.join(DATA_DIR, filename), "r") as f:
                    all_data[user_id] = json.load(f)
    except Exception as e:
        print("Error loading all users:", e)
    return all_data

