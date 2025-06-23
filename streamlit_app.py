import streamlit as st
from crew_planner import plan_tasks  # Your AI task planner
import os

st.set_page_config(page_title="Goal Tracker AI", page_icon="🚀")

st.title("🚀 Goal Tracker AI")
st.subheader("Turn your big goals into daily tasks with AI coaching")

# Input section
goal = st.text_input("🎯 Enter your goal (e.g., Learn Data Science):")
days = st.number_input("📅 How many days do you want to achieve it?", min_value=1, max_value=30, value=5)

if st.button("Create Plan"):
    if not goal.strip():
        st.warning("Please enter a goal.")
    else:
        with st.spinner("Planning your daily tasks..."):
            task_list = plan_tasks(goal, days)
            if isinstance(task_list, list):
                st.session_state['tasks'] = task_list
                st.session_state['goal'] = goal
                st.session_state['days'] = days
            else:
                st.error("❌ Task generation failed. Please try again.")

# Display results
if 'tasks' in st.session_state:
    st.success(f"📌 Plan for: **{st.session_state['goal']}** in {st.session_state['days']} days")
    for task in st.session_state['tasks']:
        st.markdown(f"**Day {task['day']}**: {task['task']}")

