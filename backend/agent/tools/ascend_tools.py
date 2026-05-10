import os
import requests
from typing import Optional
from dotenv import load_dotenv
from langchain_core.tools import tool

# Cargar variables de entorno
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
load_dotenv(os.path.join(BASE_DIR, ".env"))

# Configuración de AscendAPI (RapidAPI)
ASCEND_HOST = os.getenv("RAPIDAPI_HOST")
ASCEND_KEY = os.getenv("RAPIDAPI_KEY")
ASCEND_BASE_URL = f"https://{ASCEND_HOST}/api/v1"

ASCEND_HEADERS = {
    "X-RapidAPI-Key": ASCEND_KEY,
    "X-RapidAPI-Host": ASCEND_HOST,
}

TIMEOUT = 12

def safe_get(url: str, headers: Optional[dict] = None, params: Optional[dict] = None) -> dict:
    """Función auxiliar para realizar peticiones GET de forma segura."""
    try:
        response = requests.get(url, headers=headers, params=params, timeout=TIMEOUT)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        return {"error": str(e), "url": url}

@tool
def list_ascend_body_parts():
    """
    Lista todas las categorías de partes del cuerpo disponibles en AscendAPI.
    Útil para saber qué términos usar en la búsqueda por body_part.
    """
    url = f"{ASCEND_BASE_URL}/bodyparts"
    payload = safe_get(url, headers=ASCEND_HEADERS)
    
    if payload.get("error"):
        return payload
    
    return payload.get("data", [])

@tool
def search_ascend_exercises(
    name: Optional[str] = None,
    body_part: Optional[str] = None,
    equipment: Optional[str] = None,
    muscle: Optional[str] = None,
    limit: int = 10,
):
    """
    Busca ejercicios en la base de datos de AscendAPI.
    Permite filtrar por nombre, parte del cuerpo, equipamiento o músculo objetivo.
    Devuelve información completa: instrucciones, videos, imágenes, equipos y músculos.
    """
    params = {"limit": limit}

    if name:
        url = f"{ASCEND_BASE_URL}/exercises/name/{name.lower()}"
    elif body_part:
        url = f"{ASCEND_BASE_URL}/exercises/bodyPart/{body_part.lower()}"
    elif equipment:
        url = f"{ASCEND_BASE_URL}/exercises/equipment/{equipment.lower()}"
    elif muscle:
        url = f"{ASCEND_BASE_URL}/exercises/target/{muscle.lower()}"
    else:
        url = f"{ASCEND_BASE_URL}/exercises"

    payload = safe_get(url, headers=ASCEND_HEADERS, params=params)

    if payload.get("error"):
        return payload

    data = payload.get("data", [])
    for ex in data:
        print( {
            "source": "ascend",
            "exercise_id": ex.get("exerciseId"),
            "name": ex.get("name"),
            "overview": ex.get("overview"),
            "instructions": ex.get("instructions"),
            "video_url": ex.get("videoUrl"),
            "image_url": ex.get("imageUrl"),
            "equipments": ex.get("equipments", []),
            "body_parts": ex.get("bodyParts", []),
            "exercise_type": ex.get("exerciseType"),
            "target_muscles": ex.get("targetMuscles", []),
            "secondary_muscles": ex.get("secondaryMuscles", []),
        })
    return [
        {
            "source": "ascend",
            "exercise_id": ex.get("exerciseId"),
            "name": ex.get("name"),
            "overview": ex.get("overview"),
            "instructions": ex.get("instructions"),
            "video_url": ex.get("videoUrl"),
            "image_url": ex.get("imageUrl"),
            "equipments": ex.get("equipments", []),
            "body_parts": ex.get("bodyParts", []),
            "exercise_type": ex.get("exerciseType"),
            "target_muscles": ex.get("targetMuscles", []),
            "secondary_muscles": ex.get("secondaryMuscles", []),
        }
        for ex in data
    ]