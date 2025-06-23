# crew_planner.py

import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def plan_tasks(goal, days):
    import json

    prompt = f"""
    Break down the goal "{goal}" into {days} daily learning tasks.
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
        structured_tasks = json.loads(reply)
        # ✅ Convert to readable text
        task_text = [f"Day {task['day']}: {task['task']}" for task in structured_tasks]
        return task_text
    except Exception as e:
        print("⚠️ JSON Parse Error:", e)
        return ["Day 1: Sorry, task breakdown failed!"]

