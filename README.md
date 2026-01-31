# Goal-Oriented Autonomous Task Orchestrator

## Overview
This project is a Python-based autonomous task orchestration system designed to help users stay aligned with personal or professional goals through scheduled, goal-driven automation.

The system plans tasks, schedules execution, and delivers context-aware outputs without requiring repeated manual prompts. It demonstrates early-stage Agentic AI concepts such as planning, orchestration, and autonomous execution loops.

---

## Problem Statement
Most productivity and reminder systems rely on static rules or manual triggers. This project explores how autonomous systems can:
- Understand user goals
- Plan supporting actions
- Execute tasks on a schedule
- Deliver meaningful outputs automatically

---

## System Architecture

### Core Components
- **Planner Module (`crew_planner.py`)**  
  Translates user goals into executable task plans

- **Scheduler (`scheduler.py`, `scheduled_tasks.py`)**  
  Handles time-based autonomous execution

- **Task Execution Engine (`scheduled_task_sender.py`)**  
  Triggers planned tasks and delivers outputs

- **Content Generator (`motivation_quotes.py`)**  
  Generates contextual motivational content

- **User Context & Memory**  
  Maintained using `user_settings.json` and loaders

- **Delivery Integration**  
  Supports external delivery mechanisms (e.g., WhatsApp utilities)

- **User Interface**  
  Streamlit-based UI for configuration and monitoring

---

## Key Features
- Goal-driven task planning
- Autonomous scheduled execution
- Context persistence across runs
- Modular and extensible design
- Minimal human intervention after setup

---

## Tech Stack
- Python
- Streamlit
- Scheduling libraries
- JSON-based persistence
- API-based messaging integrations

---

## Project Structure

