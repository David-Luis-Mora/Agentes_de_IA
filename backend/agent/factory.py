import asyncio
import os
from langchain_ollama import ChatOllama
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.agents import create_agent
from .tools.wger_tools import get_exercises_by_muscle, get_exercise_details, get_muscles
from .tools.rag_tools import search_knowledge_base
from .tools.db_tools import get_user_profile, update_user_profile
from .tools.nutrition_tools import search_nutrition_knowledge

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MCP_SERVER_PATH = os.path.join(BASE_DIR, "gym-tracker-mcp", "dist", "index.js")

async def get_gym_agent():
    """
    Creates and returns the unified GymAI Agent (Fitness + Nutrition).
    """
    # 1. Initialize MCP Client for external tools
    mcp_client = MultiServerMCPClient({
        "gym_tracker": {
            "transport": "stdio",
            "command": "node",
            "args": [MCP_SERVER_PATH]
        }
    })
    
    # 2. Get tools from MCP servers
    try:
        mcp_tools = await mcp_client.get_tools()
    except Exception as e:
        print(f"Warning: Could not connect to MCP server: {e}")
        mcp_tools = []
    
    # 3. Combine all tools
    all_tools = mcp_tools + [
        get_exercises_by_muscle,
        get_exercise_details,
        get_muscles,
        search_knowledge_base, # RAG Gimnasio
        search_nutrition_knowledge, # RAG Nutrición (Vectorizado)
        get_user_profile,
        update_user_profile
    ]
    
    # 4. Configure LLM (Local Ollama)
    # Using Qwen 2.5 because it supports tools and reasoning efficiently
    llm = ChatOllama(
        model="qwen2.5:7b",
        reasoning=True,
        num_ctx=12000,
    )
    
    # 5. Create Unified Agent
    agent = create_agent(
        model=llm,
        tools=all_tools,
        system_prompt=(
            "Eres 'GymAI', un experto integral en Fitness, Entrenamiento y Nutrición Deportiva.\n\n"
            "Tus responsabilidades incluyen:\n"
            "1. ENTRENAMIENTO: Recomendar rutinas y ejercicios usando Wger y tu base de conocimientos de gimnasio.\n"
            "2. NUTRICIÓN: Proporcionar planes y consejos dietéticos usando tu base de conocimientos de nutrición (RAG).\n"
            "3. SEGUIMIENTO: Consultar el perfil del usuario y el Gym Tracker (MCP) para personalizar cada respuesta.\n\n"
            "Reglas Críticas:\n"
            "- Antes de dar cualquier consejo, consulta el perfil del usuario (peso, altura, objetivo).\n"
            "- Si el usuario pregunta por nutrición o dietas, SIEMPRE termina tu respuesta con el siguiente aviso:\n"
            "  'NOTA: Esta es una recomendación general basada en literatura deportiva. Para un plan nutricional personalizado, consulte con un especialista.'\n"
            "- Siempre responde en Español de forma profesional y motivadora.\n"
            "- Si te falta información (como el peso o el objetivo), pídela antes de decidir."
        )
    )
    
    return agent
