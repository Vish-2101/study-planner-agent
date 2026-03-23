import json
from crewai.tools import tool

@tool("study_time_calculator")
def study_time_calculator(subjects_json: str, days: int, daily_hours: int) -> str:
    """
    Calculates weighted study hours distribution based on chapters left.
    
    Args:
        subjects_json (str): A JSON string representing a list of subjects. 
                             Format: '[{"name": "AI", "total": 10, "left": 5}]'
        days (int): The total number of days available until the exam.
        daily_hours (int): The number of hours you can study per day.

    Returns:
        str: A string representation of the calculated hours for each subject.
    """
    try:
        subjects_data = json.loads(subjects_json)
    except json.JSONDecodeError:
        return "Error: subjects_json must be a valid JSON string containing the subjects array."

    total_time_available = days * daily_hours
    
    # Calculate total weight based on chapters left. 
    # Use max(1, left) to ensure even subjects with 0 chapters left get a tiny review slot
    total_weight = 0
    weights = []
    for sub in subjects_data:
        left = int(sub.get('left', 0))
        weight = max(1, left) 
        total_weight += weight
        weights.append((sub['name'], weight))

    if total_weight == 0:
        return "Error: No valid subjects provided."

    distribution = {}
    for name, weight in weights:
        # Calculate proportional hours and round to 1 decimal place
        allocated_hours = round((weight / total_weight) * total_time_available, 1)
        distribution[name] = allocated_hours

    result = {
        "total_study_hours": total_time_available,
        "recommended_distribution": distribution
    }

    return str(result)