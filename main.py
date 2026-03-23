import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, LLM
from planner_tools import study_time_calculator
from calendar_tool import google_calendar_tool
from datetime import datetime, timedelta

# Load environment variables
load_dotenv()

# Determine which LLM to use based on available API keys
# Prefer Gemini since we are in a Gemini ecosystem, but fall back to OpenAI if it's there
llm = None
if os.getenv("GEMINI_API_KEY"):
    llm = LLM(model="gemini/gemini-3-flash-preview", api_key=os.getenv("GEMINI_API_KEY"))
elif os.getenv("OPENAI_API_KEY"):
    llm = LLM(model="gpt-4o-mini", api_key=os.getenv("OPENAI_API_KEY"))
else:
    print("WARNING: Neither GEMINI_API_KEY nor OPENAI_API_KEY was found in the environment variables.")
    print("Please create a .env file and add one of these keys. CrewAI will default to OpenAI and might fail.")

# Note: The tools are now decorated functions, not instantiated classes
calculator_tool = study_time_calculator
calendar_tool = google_calendar_tool

# Calculate the actual dates to help the agent pass dynamic dates to the calendar
today_date = datetime.now()
exam_date = today_date + timedelta(days=5)

planner_agent = Agent(
    role="AI Study Planner",
    goal="Create efficient study schedules and add them to Google Calendar",
    backstory=(
        "You are an expert academic planner that helps students prepare for exams "
        "by creating balanced study schedules. You take the availability of the student "
        "and their subjects into account, structuring the sessions day by day."
    ),
    tools=[calculator_tool, calendar_tool],
    llm=llm,
    verbose=True
)

task = Task(
    description=(
        f"""
Create a study schedule starting from today ({today_date.strftime("%Y-%m-%d")}) until the exam ({exam_date.strftime("%Y-%m-%d")}).

Subjects: AI, ML, Cloud Computing
Days until exam: 5
Daily study hours: 4

Steps:
1. Use the `study_time_calculator` tool to figure out total study hours and allocate hours per subject.
2. Based on step 1, create a daily study plan for each of the 5 days. For each day, schedule specific blocks for subjects.
3. Use the `google_calendar_tool` to ADD EACH study session to Google Calendar. Make sure to use the correct date (YYYY-MM-DD form) 
   and a logical start_hour (e.g., 10 for 10 AM, 14 for 2PM) and duration. Do NOT overlap sessions.
"""
    ),
    expected_output="A full valid study schedule outlining subjects day by day, and confirmations that the calendar events were successfully created.",
    agent=planner_agent
)

crew = Crew(
    agents=[planner_agent],
    tasks=[task],
    verbose=True
)

if __name__ == "__main__":
    print(f"Starting the AI Study Planner Crew using LLM: {llm.model if llm else 'Default OpenAI'}")
    result = crew.kickoff()
    print("\nFinal Result\n")
    print(result)