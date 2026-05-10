# import requests
# from langchain_core.tools import tool

# BASE_URL = "https://wger.de/api/v2"

# @tool
# def get_exercises_by_muscle(muscle_id: int):
#     """
#     Obtiene una lista de ejercicios filtrada por músculo usando Wger info.
#     IDs comunes: 1 (Pecho), 2 (Hombros), 10 (Cuádriceps), 12 (Espalda).
#     """
#     url = f"{BASE_URL}/exerciseinfo/?muscles={muscle_id}&language=2"
#     response = requests.get(url)
#     if response.status_code == 200:
#         results = response.json().get('results', [])
#         return [{
#             "id": r.get('id'),
#             "name": r.get('name'),
#             "category": r.get('category', {}).get('name'),
#             "primary_muscles": [m.get('name') for m in r.get('muscles', [])],
#             "secondary_muscles": [m.get('name') for m in r.get('muscles_secondary', [])]
#         } for r in results[:10]]
#     return f"Error: {response.status_code}"

# @tool
# def get_exercise_details_rich(exercise_id: int):
#     """
#     Obtiene detalles técnicos COMPLETOS (Músculos, Categoría, Equipo) de Wger.
#     """
#     url = f"{BASE_URL}/exerciseinfo/{exercise_id}/"
#     response = requests.get(url)
#     if response.status_code == 200:
#         data = response.json()
#         return {
#             "id": data.get('id'),
#             "name": data.get('name'),
#             "description": data.get('description'),
#             "category": data.get('category', {}).get('name'),
#             "primary_muscles": [m.get('name') for m in data.get('muscles', [])],
#             "secondary_muscles": [m.get('name') for m in data.get('muscles_secondary', [])],
#             "equipment": [e.get('name') for e in data.get('equipment', [])]
#         }
#     return f"Error: {response.status_code}"

# @tool
# def get_wger_video(exercise_id: int):
#     """
#     Busca el video oficial en Wger para un ejercicio.
#     Retorna la URL directa del video .mp4/.mov si existe.
#     """
#     url = f"{BASE_URL}/video/?exercise={exercise_id}"
#     response = requests.get(url)
#     if response.status_code == 200:
#         results = response.json().get('results', [])
#         if results:
#             # Preferimos el video principal
#             video_data = next((v for v in results if v.get('is_main')), results[0])
#             return video_data.get('video')
#     return "No video found in Wger"


