import json
import os

DATA_FILE = "goal_data.json"

def load_goal_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {}
    return {}

def save_goal_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)