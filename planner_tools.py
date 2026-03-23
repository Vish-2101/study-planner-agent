from crewai.tools import tool

@tool("study_time_calculator")
def study_time_calculator(subjects: str, days: int, daily_hours: int) -> str:
    """
    Calculates study hours distribution among a given list of subjects.
    
    Args:
        subjects (str): A comma-separated string of subjects (e.g., "AI, ML, Cloud Computing").
        days (int): The total number of days available until the exam.
        daily_hours (int): The number of hours you can study per day.

    Returns:
        str: A string representation of a dictionary containing the total hours, 
             hours per subject, and the list of subjects.
    """
    subjects_list = [s.strip() for s in subjects.split(",")]

    total_hours = days * daily_hours
    hours_per_subject = total_hours / len(subjects_list) if len(subjects_list) > 0 else 0

    result = {
        "total_hours": total_hours,
        "hours_per_subject": hours_per_subject,
        "subjects": subjects_list
    }

    return str(result)