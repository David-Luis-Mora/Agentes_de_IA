import asyncio
import os
from langchain_ollama import ChatOllama
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.agents import create_agent
from langchain_core.tools import tool
from asgiref.sync import sync_to_async

# Importación de herramientas externas
from .tools.wger_tools import get_exercises_by_muscle, get_exercise_details, get_muscles, get_exercise_video
from .tools.rag_tools import search_knowledge_base
from .tools.nutrition_tools import search_nutrition_knowledge

# Rutas
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MCP_SERVER_PATH = os.path.join(BASE_DIR, "gym-tracker-mcp", "dist", "index.js")

# --- FUNCIONES DE APOYO (Fuera de la fábrica para legibilidad) ---

@sync_to_async
def fetch_user_context(user):
    """Obtiene los datos del perfil de forma segura para async."""
    try:
        p = user.profile
        return {
            "nickname": p.nickname or user.username,
            "weight": p.weight,
            "height": p.height,
            "days_per_week": p.days_per_week,
            "time_per_session": p.time_per_session,
            "fitness_goal": p.fitness_goal,
            "experience_level": p.experience_level
        }
    except Exception:
        return None

def format_profile_context(data, username):
    """Formatea la información del perfil para el prompt del sistema."""
    if not data:
        return "Usuario actual: Desconocido (Pide los datos si son estrictamente necesarios)."
    
    def val(v, unit=""):
        return f"{v}{unit}" if v else "No especificado"

    return (
        f"DATOS ACTUALES DEL USUARIO:\n"
        f"- Nombre/Nick: {data['nickname']}\n"
        f"- Peso: {val(data['weight'], 'kg')}\n"
        f"- Altura: {val(data['height'], 'cm')}\n"
        f"- Días disponibles: {val(data['days_per_week'], ' días/semana')}\n"
        f"- Tiempo por sesión: {val(data['time_per_session'], ' min')}\n"
        f"- Objetivo: {val(data['fitness_goal'])}\n"
        f"- Nivel de experiencia: {val(data['experience_level'])}\n"
    )

# --- FÁBRICA DE HERRAMIENTAS (Para evitar anidamiento excesivo) ---

def create_user_bound_tools(user):
    """
    Crea las herramientas que necesitan estar vinculadas al contexto del usuario.
    Se mantienen aquí para capturar la instancia 'user'.
    """
    @tool
    def get_my_profile():
        """Consulta mi perfil actual (peso, altura, objetivo, etc.) de forma automática."""
        p = user.profile
        return {
            "username": user.username,
            "weight": p.weight,
            "height": p.height,
            "days_per_week": p.days_per_week,
            "time_per_session": p.time_per_session,
            "fitness_goal": p.fitness_goal,
            "experience_level": p.experience_level
        }

    @tool
    def update_my_profile(**kwargs):
        """Actualiza mi perfil actual. Puedes cambiar: weight, height, days_per_week, etc."""
        p = user.profile
        for key, value in kwargs.items():
            if hasattr(p, key):
                setattr(p, key, value)
        p.save()
        return "Perfil actualizado con éxito."

    @tool
    def save_workout_plan(plan: list):
        """
        Guarda un plan de entrenamiento completo (puede ser uno o varios días).
        'plan' debe ser una lista de diccionarios. Cada diccionario debe tener:
        - 'day_of_week': int (0=Lunes, 1=Martes, ..., 6=Domingo)
        - 'exercises': lista de objetos con 'name', 'wger_id', 'description', 'video_url'
        - 'routine_name': opcional (por defecto será 'Rutina')
        """
        from core.models import Routine, RoutineExercise
        
        results = []
        for day_data in plan:
            day = day_data.get('day_of_week')
            name = day_data.get('routine_name', 'Rutina')
            exercises = day_data.get('exercises', [])
            
            if day is None:
                continue
            
            # Limpiar rutina previa de ese día
            Routine.objects.filter(user=user, day_of_week=day).delete()
            
            # Crear nueva rutina
            r = Routine.objects.create(user=user, day_of_week=day, name=name)
            
            for idx, ex in enumerate(exercises):
                if isinstance(ex, dict):
                    ex_name = ex.get('name', 'Ejercicio')
                    wger_id = ex.get('wger_id')
                    desc = ex.get('description', '')
                    video = ex.get('video_url')
                else:
                    ex_name = str(ex)
                    wger_id = None
                    desc = ""
                    video = None

                RoutineExercise.objects.create(
                    routine=r,
                    wger_id=wger_id,
                    name=ex_name,
                    description=desc,
                    video_url=video,
                    order=idx
                )
            results.append(f"Día {day}")
            
        return f"Plan guardado correctamente para: {', '.join(results)}."

    return [get_my_profile, update_my_profile, save_workout_plan]

# --- FUNCIÓN PRINCIPAL ---

async def get_gym_agent(user):
    """
    Crea y devuelve el Agente GymAI unificado.
    """
    # 1. Preparar contexto
    user_data = await fetch_user_context(user)
    profile_context = format_profile_context(user_data, user.username)
    print(f"DEBUG: Contexto cargado para {user.username}")

    # 2. Clientes Externos (MCP)
    mcp_client = MultiServerMCPClient({
        "gym_tracker": {
            "transport": "stdio",
            "command": "node",
            "args": [MCP_SERVER_PATH]
        }
    })
    
    try:
        mcp_tools = await mcp_client.get_tools()
    except Exception as e:
        print(f"Warning: MCP Error: {e}")
        mcp_tools = []
    
    # 3. Consolidar todas las herramientas
    user_tools = create_user_bound_tools(user)
    all_tools = mcp_tools + user_tools + [
        get_exercises_by_muscle,
        get_exercise_details,
        get_muscles,
        get_exercise_video,
        search_knowledge_base,
        search_nutrition_knowledge
    ]
    
    # 4. Configurar el LLM
    llm = ChatOllama(
        model="qwen3.6:35b",
        reasoning=False,
        num_ctx=8000,
    )
    
    # 5. Crear el Agente
    agent = create_agent(
        model=llm,
        tools=all_tools,
        system_prompt=(
            "Eres 'GymAI', un experto integral en Fitness, Entrenamiento y Nutrición Deportiva.\n\n"
            "CONTEXTO DEL USUARIO:\n"
            f"{profile_context}\n\n"
            "Reglas Críticas de Comportamiento:\n"
            "- YA TIENES el contexto del usuario arriba. NO pidas peso, altura u objetivos si ya están presentes.\n"
            "- Si te falta información, búscala solo si es estrictamente necesaria para la tarea.\n"
            "- Si el usuario confirma que la rutina le gusta (ej: 'Sí', 'Ok', 'Guárdala'), usa 'save_workout_plan' para guardarla automáticamente.\n"
            "- Identifica los días de la semana basándote en la conversación (0=Lunes, 6=Domingo) y asígnalos al parámetro 'day_of_week'.\n"
            "- Para el nombre de la rutina, usa siempre 'Rutina' a menos que el usuario pida otro nombre específico.\n"
            "- No preguntes '¿qué día quieres guardarla?' si ya se ha mencionado el día o si es obvio por el contexto.\n"
            "- Asegúrate de incluir todos los detalles (ID, descripción, video) en la lista de ejercicios al guardar.\n"
            "- Siempre responde en Español de forma profesional y motivadora.\n"
            "- No tardes tanto en pensar las cosas, ve paso a paso y vete dando cuenta de lo que necesitas para realizar la tarea."
            "- Maximo tiene que tarda en 2 minutos en responder."

        )
    )
    
    return agent
