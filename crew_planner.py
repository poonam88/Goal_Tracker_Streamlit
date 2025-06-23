# crew_planner.py

import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def plan_tasks(goal, days):
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

    # Parse as JSON from assistant message
    import json
    reply = response.choices[0].message.content
    try:
        return json.loads(reply)
    except:
        return [{"day": 1, "task": "Sorry, task breakdown failed!"}]

