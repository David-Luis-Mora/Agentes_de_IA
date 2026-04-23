import asyncio
from mcp import ClientSession, StdioServerParameters, stdio_client
from langchain_core.tools import tool

MCP_SERVER_PATH = "/home/inta@informatica.edu/Escritorio/Agentes_de_IA/gym-tracker-mcp/dist/index.js"

async def run_mcp_tool(tool_name: str, arguments: dict):
    # This requires the .env variables to be set in the environment
    server_params = StdioServerParameters(command="node", args=[MCP_SERVER_PATH])
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            result = await session.call_tool(tool_name, arguments)
            return result

@tool
def get_workout_history():
    """
    Retrieves recent workouts with specific details on exercises, weights, and repetitions.
    Connects to the Gym Tracker MCP server.
    """
    try:
        # Run in a synchronous wrapper for LangChain if needed, or use asyncio.run
        return asyncio.run(run_mcp_tool("get_workout_history", {}))
    except Exception as e:
        return f"Error connecting to Gym Tracker MCP: {str(e)}. Make sure credentials are set in .env"

@tool
def get_exercise_progress(exercise_name: str):
    """
    Shows the progression history for a specific exercise (max weight, volume, trends).
    """
    try:
        return asyncio.run(run_mcp_tool("get_exercise_progress", {"exerciseName": exercise_name}))
    except Exception as e:
        return f"Error: {str(e)}"
