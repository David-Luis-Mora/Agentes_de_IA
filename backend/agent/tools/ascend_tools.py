import os
import requests
from dotenv import load_dotenv
from langchain_core.tools import tool

# Load environment variables
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
load_dotenv(os.path.join(BASE_DIR, ".env"))

RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")
RAPIDAPI_HOST = os.getenv("RAPIDAPI_HOST")

HEADERS = {
    "X-RapidAPI-Key": RAPIDAPI_KEY,
    "X-RapidAPI-Host": RAPIDAPI_HOST
}

BASE_URL = f"https://{RAPIDAPI_HOST}/api/v1"

@tool
def search_ascend_exercises(name: str = None, body_part: str = None, equipment: str = None, muscle: str = None, limit: int = 10):
    """
    Busca ejercicios en la base de datos AscendAPI (ExerciseDB con imágenes y videos).
    Permite filtrar por nombre, parte del cuerpo (body_part), equipamiento (equipment) o músculo objetivo (muscle).
    Retorna una lista de ejercicios con sus IDs, nombres y previsualizaciones.
    """
    params = {"limit": limit}
    
    if name:
        url = f"{BASE_URL}/exercises/name/{name.lower()}"
    elif body_part:
        url = f"{BASE_URL}/exercises/bodyPart/{body_part.lower()}"
    elif equipment:
        url = f"{BASE_URL}/exercises/equipment/{equipment.lower()}"
    elif muscle:
        url = f"{BASE_URL}/exercises/target/{muscle.lower()}"
    else:
        url = f"{BASE_URL}/exercises"
    
    try:
        response = requests.get(url, headers=HEADERS, params=params)
        if response.status_code == 200:
            data = response.json().get('data', [])
            # Retornamos los campos clave directamente en la búsqueda para que la IA
            # NO tenga que llamar a 'details' por cada ejercicio (ahorra mucho tiempo).
            return [
                {
                    "exerciseId": ex.get("exerciseId"),
                    "name": ex.get("name"),
                    "overview": ex.get("overview"),
                    "instructions": ex.get("instructions"),
                    "videoUrl": ex.get("videoUrl"),
                    "imageUrl": ex.get("imageUrl"),
                    "primaryMuscle": ex.get("primaryMuscle"),
                    "secondaryMuscle": ex.get("secondaryMuscle"),
                    "category": ex.get("category"),
                    "equipment": ex.get("equipment")
                } for ex in data
            ]

        return f"Error: {response.status_code}"
    except Exception as e:
        return f"Error: {str(e)}"

@tool
def get_ascend_exercise_details(exercise_id: str):
    """
    Obtiene detalles completos (HD) de un ejercicio de AscendAPI.
    """
    url = f"{BASE_URL}/exercises/{exercise_id}"
    try:
        response = requests.get(url, headers=HEADERS)
        if response.status_code == 200:
            data = response.json().get('data', {})
            return {
                "name": data.get("name"),
                "overview": data.get("overview"),
                "videoUrl": data.get("videoUrl"),
                "imageUrl": data.get("imageUrl"),
                "instructions": data.get("instructions"),
                "primaryMuscle": data.get("primaryMuscle"),
                "secondaryMuscle": data.get("secondaryMuscle"),
                "category": data.get("category")
            }
        return f"Error: {response.status_code}"
    except Exception as e:
        return f"Error: {str(e)}"


@tool
def list_ascend_body_parts():
    """
    Lista todas las categorías de partes del cuerpo disponibles en AscendAPI.
    """
    url = f"{BASE_URL}/bodyparts"
    try:
        response = requests.get(url, headers=HEADERS)
        if response.status_code == 200:
            return response.json().get('data', [])
        return f"Error: {response.status_code}"
    except Exception as e:
        return f"Error: {str(e)}"
