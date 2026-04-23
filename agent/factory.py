from langchain_openai import ChatOpenAI
from langchain_classic.agents import AgentExecutor
from langchain_classic.agents.openai_functions_agent.base import create_openai_functions_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from .tools.wger_tools import get_exercises_by_muscle, get_exercise_details, get_muscles
from .tools.mcp_tools import get_workout_history, get_exercise_progress
from .tools.rag_tools import search_knowledge_base
from .tools.db_tools import get_user_profile, update_user_profile

def get_gym_agent():
    # Configure LLM (Local Ollama)
    llm = ChatOpenAI(
        model="qwen3:8b ", # Or the model the user has available
        base_url="http://localhost:11434/v1",
        # api_key="ollama", # Placeholder
        temperature=0.7
    )

    tools = [
        get_exercises_by_muscle,
        get_exercise_details,
        get_muscles,
        get_workout_history,
        get_exercise_progress,
        search_knowledge_base,
        get_user_profile,
        update_user_profile
    ]

    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a highly professional Gym Coach and Fitness Expert. 
        Your goal is to recommend routines and exercises based on the user's profile and preferences.
        
        Guidelines:
        1. Always check the user's profile (weight, height, goals, availability) before making recommendations.
        2. Use the Knowledge Base (RAG) to provide scientific justification for your advice (mention progressive overload, volume, etc.).
        3. Use Wger tools to find specific exercises.
        4. Use Gym Tracker (MCP) to check the user's past performance and adapt the routine.
        5. If the user hasn't set their profile, ask for their weight, height, and goals.
        6. Be encouraging but professional. Focus on safety and consistency.
        """),
        MessagesPlaceholder(variable_name="chat_history"),
        ("user", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])

    agent = create_openai_functions_agent(llm, tools, prompt)
    
    return AgentExecutor(agent=agent, tools=tools, verbose=True)
