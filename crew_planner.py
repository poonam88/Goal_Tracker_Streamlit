from crewai import Crew, Agent, Task
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4", temperature=0.5)

def plan_tasks(goal: str, days: int):
    search_tool = DuckDuckGoSearchRun()

    planner = Agent(
        role="Goal Planner",
        goal="Break big goals into smaller, daily tasks",
        backstory="You're an expert at planning step-by-step learning journeys.",
        tools=[search_tool],
        llm=llm,
        allow_delegation=False
    )

    task = Task(
        description=f"Create a {days}-day plan for this goal: {goal}",
        expected_output="Return a JSON array like: ['Day 1: ...', 'Day 2: ...', ..., 'Day N: ...']",
        agent=planner
    )

    crew = Crew(agents=[planner], tasks=[task], verbose=True)
    result = crew.run()

    try:
        # Try to extract list from string
        tasks = eval(result.strip())
        if isinstance(tasks, list):
            return tasks
        else:
            return [f"Day {i+1}: {line}" for i, line in enumerate(result.split('\n'))]
    except:
        return [f"Day {i+1}: {line}" for i, line in enumerate(result.split('\n'))]
