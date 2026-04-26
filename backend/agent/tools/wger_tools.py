import requests
from langchain_core.tools import tool

BASE_URL = "https://wger.de/api/v2"

@tool
def get_exercises_by_muscle(muscle_id: int):
    """
    Obtiene una lista de ejercicios de la API de Wger filtrada por ID de músculo.
    IDs de Músculos: 1 (Bíceps), 2 (Hombros), 3 (Pecho), 4 (Espalda), 9 (Tríceps), 10 (Cuádriceps), 11 (Isquiotibiales), 12 (Gemelos).
    """
    url = f"{BASE_URL}/exercise/?muscle={muscle_id}&language=2"  # el lenguaje 2 es inglés (la API tiene más datos en inglés)
    response = requests.get(url)
    if response.status_code == 200:
        results = response.json().get('results', [])
        return [{"id": r.get('id'), "nombre": r.get('name', 'N/A'), "descripcion": r.get('description', '')} for r in results]
    return f"Error: {response.status_code}"

@tool
def get_exercise_details(exercise_id: int):
    """
    Obtiene información detallada sobre un ejercicio específico mediante su ID.
    """
    url = f"{BASE_URL}/exercise/{exercise_id}/"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return f"Error: {response.status_code}"

@tool
def get_muscles():
    """
    Obtiene la lista de músculos y sus respectivos IDs.
    """
    url = f"{BASE_URL}/muscle/"
    response = requests.get(url)
    if response.status_code == 200:
        results = response.json().get('results', [])
        return [{"id": r.get('id'), "nombre": r.get('name', 'N/A')} for r in results]
    return f"Error: {response.status_code}"

@tool
def get_exercise_video(exercise_id: int):
    """
    Busca si existe un video demostrativo para un ejercicio específico.
    """
    url = f"{BASE_URL}/exercisevideo/?exercise={exercise_id}"
    response = requests.get(url)
    if response.status_code == 200:
        results = response.json().get('results', [])
        if results:
            video = results[0].get('video')
            return video if video else "No se encontró video para este ejercicio."
    return "No se encontró video para este ejercicio."
