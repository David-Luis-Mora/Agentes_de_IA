import asyncio
import os
from langchain_ollama import ChatOllama
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.agents import create_agent
from langchain_core.tools import tool
from asgiref.sync import sync_to_async
from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver

# Importación de herramientas externas
from .tools.wger_tools import get_exercises_by_muscle, get_exercise_details_rich, get_wger_video
from .tools.knowledge_tools import (
    search_training_advice, 
    search_exercise_technique, 
    search_recovery_and_rest, 
    search_nutrition_articles,
    index_new_knowledge
)
from .tools.user_tools import get_my_profile, update_my_profile, save_workout_plan, user_ctx, request_ctx
from .tools.ascend_tools import search_ascend_exercises, get_ascend_exercise_details, list_ascend_body_parts


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
    print(f"DEBUG: Contexto cargado para {user.username}")
    
    mcp_tools = []
    
    # 3. Consolidar todas las herramientas
    all_tools =[
        get_my_profile,
        update_my_profile,
        save_workout_plan,
        get_exercises_by_muscle,
        get_exercise_details_rich,
        get_wger_video,
        search_training_advice,
        search_exercise_technique,
        search_recovery_and_rest,
        search_nutrition_articles,
        index_new_knowledge,
        search_ascend_exercises,
        get_ascend_exercise_details,
        list_ascend_body_parts
    ]

    
    # 4. Configurar el LLM
    llm = ChatOllama(
        model="qwen3.6:35b",
        # model="gemma4:26b",
        # model="qwen3:14b",
        # model="gemma3:12b",
        reasoning=False,
        # num_ctx=32000,
        # num_ctx=16000,
        num_ctx=12000,
        # num_ctx=8000,
        # base_url="http://192.168.117.48:11434"
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
            "1. ENTRENAMIENTO: Usa 'search_training_advice' para principios de hipertrofia, series, repeticiones y sobrecarga.\n"
            "2. TÉCNICA: Usa 'search_exercise_technique' para saber CÓMO ejecutar un ejercicio correctamente.\n"
            "3. RECUPERACIÓN: Usa 'search_recovery_and_rest' si el usuario está cansado o pregunta por descanso.\n"
            "4. NUTRICIÓN: Usa 'search_nutrition_articles' para consejos nutricionales.\n"
            "5. ESTRATEGIA HÍBRIDA DE DATOS (Calidad Máxima):\n"
            "   - IMÁGENES: Usa 'search_ascend_exercises' para obtener la 'imageUrl'. Son visualmente superiores.\n"
            "   - VÍDEOS: Usa 'get_wger_video' para obtener la URL oficial (.mp4/.mov). NO uses los vídeos de AscendAPI.\n"
            "   - METADATOS: Usa Wger para 'category', 'primary_muscles' y 'secondary_muscles'.\n"
            "   - SERIES Y REPS: DEBES generar obligatoriamente el campo 'sets' como una lista de objetos: [{'reps': 12, 'weight': 20}, {'reps': 12, 'weight': 20}]. Ajusta el peso y repeticiones según el nivel del usuario.\n\n"

            "REGLAS PARA GUARDAR RUTINAS:\n"
            "1. Cuando el usuario acepte una rutina, LLAMA inmediatamente a 'save_workout_plan'.\n"
            "2. PROHIBIDO decir que has guardado algo si NO has ejecutado la herramienta primero.\n"
            "3. Debes inferir el 'day_of_week' (0=Lunes, 6=Domingo).\n"
            "4. En 'exercises', combina: 'imageUrl' de Ascend, 'videoUrl' de Wger, metadatos de Wger y tu generación de 'sets'.\n\n"





            "Reglas Críticas de Comportamiento:\n"
            "- YA TIENES el contexto del usuario arriba. NO pidas peso, altura u objetivos si ya están presentes.\n"
            "- Si el usuario confirma que la rutina le gusta, usa 'save_workout_plan' inmediatamente sin volver a preguntar.\n"
            "- Responde siempre en Español de forma profesional, clara y motivadora.\n"
            "- No tardar más de 2 minutos en responder."
        )
    )
    
    return agent
