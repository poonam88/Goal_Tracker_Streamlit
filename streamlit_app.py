import streamlit as st
from crew_planner import plan_tasks
import json
import os

# Set up the Streamlit app
st.set_page_config(page_title="Goal Tracker AI", layout="centered")
st.title("🎯 Goal Tracker AI")
st.markdown("Break your big goals into daily tasks using CrewAI 💡")

# Goal Input Section
goal = st.text_input("📌 Enter your goal:", placeholder="e.g., Learn Data Science")
days = st.number_input("🗓️ Days to complete the goal:", min_value=1, max_value=30, value=5)

# Action Button
if st.button("🚀 Generate Plan"):
    if not goal:
        st.warning("Please enter a goal to proceed.")
    else:
        with st.spinner("Thinking..."):
            tasks = plan_tasks(goal, days)

            # Save to JSON file
            data = {"goal": goal, "days": days, "tasks": tasks}
            with open("goal_data.json", "w") as f:
                json.dump(data, f, indent=2)

            st.success("✅ Goal plan generated and saved!")
            st.markdown("### 📋 Your Daily Tasks")
            for i, task in enumerate(tasks, start=1):
                for task in tasks:
                    st.write(task)
