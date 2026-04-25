import requests
from langchain_core.tools import tool

BASE_URL = "https://wger.de/api/v2"

@tool
def get_exercises_by_muscle(muscle_id: int):
    """
    Fetches a list of exercises from Wger API filtered by muscle ID.
    Muscle IDs: 1 (Biceps), 2 (Shoulders), 3 (Chest), 4 (Back), 9 (Triceps), 10 (Quads), 11 (Hamstrings), 12 (Calves).
    """
    url = f"{BASE_URL}/exercise/?muscle={muscle_id}&language=2"  # language 2 is English
    response = requests.get(url)
    if response.status_code == 200:
        results = response.json().get('results', [])
        return [{"id": r['id'], "name": r['name'], "description": r['description']} for r in results]
    return f"Error: {response.status_code}"

@tool
def get_exercise_details(exercise_id: int):
    """
    Fetches detailed information about a specific exercise by ID.
    """
    url = f"{BASE_URL}/exercise/{exercise_id}/"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return f"Error: {response.status_code}"

@tool
def get_muscles():
    """
    Fetches the list of muscles and their IDs.
    """
    url = f"{BASE_URL}/muscle/"
    response = requests.get(url)
    if response.status_code == 200:
        results = response.json().get('results', [])
        return [{"id": r['id'], "name": r['name']} for r in results]
    return f"Error: {response.status_code}"
