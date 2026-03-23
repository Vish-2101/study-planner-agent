import os
import json
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, LLM
from planner_tools import study_time_calculator
from calendar_tool import google_calendar_tool
from datetime import datetime, timedelta

# Load environment variables
load_dotenv()

llm = None
if os.getenv("GEMINI_API_KEY"):
    llm = LLM(model="gemini/gemini-3-flash-preview", api_key=os.getenv("GEMINI_API_KEY"))
elif os.getenv("OPENAI_API_KEY"):
    llm = LLM(model="gpt-4o-mini", api_key=os.getenv("OPENAI_API_KEY"))
else:
    print("WARNING: Neither GEMINI_API_KEY nor OPENAI_API_KEY was found in the environment variables.")
    print("Please create a .env file and add one of these keys. CrewAI will default to OpenAI and might fail.")

calculator_tool = study_time_calculator
calendar_tool = google_calendar_tool

def run_study_planner(subjects_data: list, days: int, daily_hours: int) -> str:
    today_date = datetime.now()
    exam_date = today_date + timedelta(days=days)

    # Convert complex list to a json string to pass to the tool safely
    subjects_json_str = json.dumps(subjects_data)

    planner_agent = Agent(
        role="AI Study Planner",
        goal="Create highly optimized, priority-weighted study schedules and add them to Google Calendar.",
        backstory=(
            "You are an expert academic planner that specializes in triage and weighted scheduling. "
            "You understand that subjects with more 'chapters left' demand more time urgently. "
            "You strictly follow the mathematical distributions given to you by your calculator tool, "
            "organizing the heaviest workloads earliest in the week so the student isn't overwhelmed right before the exam."
        ),
        tools=[calculator_tool, calendar_tool],
        llm=llm,
        verbose=True
    )

    task = Task(
        description=(
            f"""
Create a priority-weighted study schedule starting from today ({today_date.strftime("%Y-%m-%d")}) until the exam ({exam_date.strftime("%Y-%m-%d")}).

Subject Data (JSON): {subjects_json_str}
Days until exam: {days}
Daily study hours: {daily_hours}

Steps:
1. Use the `study_time_calculator` tool and pass exactly the Subject Data JSON string ({subjects_json_str}), days, and daily_hours to get the recommended hour distribution.
2. Based ONLY on the mathematical distribution returned by the calculator, build a daily study plan spreading the required hours across the {days} days. Do NOT give equal time to subjects; respect the weighted distribution!
3. Schedule subjects with the most 'chapters left' (highest hours) earlier in the week.
4. Use the `google_calendar_tool` to ADD EACH study session to Google Calendar. Ensure dates use YYYY-MM-DD format, pick logical start_hours (e.g., 9 for 9AM), and make sure sessions do NOT overlap.
"""
        ),
        expected_output="The final output MUST be entirely valid HTML. Include an HTML table for the schedule, and use <h3>, <ul>, <li>, and <a href='...'> tags for the calendar confirmations. NEVER use markdown symbols like ### or ** or [Link](URL).",
        agent=planner_agent
    )

    crew = Crew(
        agents=[planner_agent],
        tasks=[task],
        verbose=True
    )

    print(f"Starting the AI Study Planner Crew using LLM: {llm.model if llm else 'Default OpenAI'}")
    result = crew.kickoff()
    return str(result)

if __name__ == "__main__":
    test_data = [
        {"name": "AI", "total": 10, "left": 8},
        {"name": "ML", "total": 5, "left": 1},
        {"name": "Cloud", "total": 8, "left": 4}
    ]
    print(run_study_planner(test_data, 5, 4))