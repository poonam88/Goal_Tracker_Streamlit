# crew_planner.py

import os
from openai import OpenAI
import json

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def plan_tasks(goal, days):
    prompt = f"""
    Break down the goal "{goal}" into {days} daily learning tasks.
    Format the output strictly as JSON:
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

    reply = response.choices[0].message.content.strip()

    try:
        tasks = json.loads(reply)
        return tasks
    except Exception as e:
        print("❌ JSON parse error:", e)
        return [{"day": 1, "task": "Sorry, task breakdown failed!"}]


