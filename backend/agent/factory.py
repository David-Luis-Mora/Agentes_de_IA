import asyncio
import os
from langchain_ollama import ChatOllama
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.agents import create_agent
from langchain_core.tools import tool
from asgiref.sync import sync_to_async
from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver

# Importación de herramientas externas
from .tools.knowledge_tools import (
    search_training_advice, 
    search_exercise_technique, 
    search_recovery_and_rest, 
    search_nutrition_articles,
    index_new_knowledge
)
from .tools.user_tools import get_my_profile, update_my_profile, save_workout_plan, user_ctx, request_ctx
from .tools.ascend_tools import (list_ascend_body_parts, search_ascend_exercises)


# Rutas
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MCP_SERVER_PATH = os.path.join(BASE_DIR, "gym-tracker-mcp", "dist", "index.js")

# --- FUNCIONES DE APOYO ---

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
        return "Usuario actual: Desconocido."
    
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

# --- FUNCIÓN PRINCIPAL ---

async def get_gym_agent(user, request=None, checkpointer=None):
    """
    Crea y devuelve el Agente GymAI unificado con soporte para memoria.
    """
    # 0. Establecer contexto global para las herramientas (ContextVars)
    user_ctx.set(user)
    request_ctx.set(request)

    # 1. Preparar contexto de prompt
    user_data = await fetch_user_context(user)
    profile_context = format_profile_context(user_data, user.username)
    
    # 3. Consolidar todas las herramientas
    all_tools =[
        get_my_profile,
        update_my_profile,
        save_workout_plan,
        search_training_advice,
        search_exercise_technique,
        search_recovery_and_rest,
        search_nutrition_articles,
        index_new_knowledge,
        search_ascend_exercises,
        list_ascend_body_parts,
    ]

    # 4. Configurar el LLM
    llm = ChatOllama(
        model="qwen3:14b",
        reasoning=False,
        num_ctx=8000,
    )
    
    # 5. Crear el Agente
    agent = create_agent(
        model=llm,
        tools=all_tools,
        checkpointer=checkpointer,
        system_prompt=(
            "Eres 'GymAI', un experto integral en Fitness, Entrenamiento y Nutrición Deportiva.\n\n"
            "CONTEXTO DEL USUARIO:\n"
            f"{profile_context}\n\n"
            "Reglas de Oro de Conocimiento:\n"
            "1. ENTRENAMIENTO: Usa 'search_training_advice' para principios de hipertrofia y sobrecarga.\n"
            "2. TÉCNICA Y CARGAS (RAG): DEBES consultar la 'Enciclopedia_de_ejercicios_de_musculacion' mediante 'search_exercise_technique' para saber CÓMO ejecutar un ejercicio y qué SERIES/PESOS recomendar.\n"
            "3. RECUPERACIÓN Y NUTRICIÓN: Usa las herramientas de búsqueda de artículos correspondientes.\n"
            "4. DATOS DE EJERCICIOS (AscendAPI):\n"
            "   - Usa 'search_ascend_exercises' para obtener TODO: 'image_url', 'video_url', 'instructions', 'equipments' y músculos.\n"
            "   - PROHIBICIÓN CRÍTICA: Está terminantemente PROHIBIDO inventar URLs de vídeos o imágenes. NUNCA uses 'wger.com' o 'wger.de'. Usa ÚNICAMENTE las URLs que devuelva la herramienta en 'image_url' y 'video_url'.\n"
            "   - Si la herramienta no devuelve una URL válida de ExerciseDB, deja el campo vacío.\n"
            "   - SERIES Y PESOS: Genera el campo 'sets' como una lista de objetos: [{'reps': 12, 'weight': 20}, ...].\n\n"

            "REGLAS PARA GUARDAR RUTINAS:\n"
            "1. Cuando el usuario acepte una rutina, LLAMA inmediatamente a 'save_workout_plan'.\n"
            "2. PROHIBIDO decir que has guardado algo si NO has ejecutado la herramienta primero.\n"
            "3. En 'exercises', incluye la información detallada de AscendAPI (image_url, video_url) y tu generación de 'sets' basada en la Enciclopedia.\n\n"
            "Reglas Críticas de Comportamiento:\n"
            "- YA TIENES el contexto del usuario arriba. NO pidas peso, altura u objetivos si ya están presentes.\n"
            "- Responde siempre en Español de forma profesional, clara y motivadora.\n"
            "- No inventes datos técnicos; si no están en la herramienta o la enciclopedia, di que no dispones de esa información específica.\n"
        )
    )
    
    return agent
