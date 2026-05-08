from langchain_core.tools import tool
from core.models import Routine, RoutineExercise, Notification
from django.contrib import messages
from contextvars import ContextVar
import logging

logger = logging.getLogger(__name__)

# --- CONTEXTO GLOBAL SEGURO ---
# Estos nos permiten acceder al usuario y la request sin pasarlos como argumentos
user_ctx = ContextVar("user_ctx")
request_ctx = ContextVar("request_ctx")

# --- HERRAMIENTAS (Top-level, decoradas con @tool) ---

@tool
def get_my_profile():
    """Consulta tu perfil actual (peso, altura, objetivo, etc.) de forma automática."""
    user = user_ctx.get()
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
    """Actualiza tu perfil actual de usuario. Puedes cambiar campos como weight, height, fitness_goal, etc."""
    user = user_ctx.get()
    p = user.profile
    for key, value in kwargs.items():
        if hasattr(p, key):
            setattr(p, key, value)
    p.save()
    return "Perfil actualizado con éxito."

@tool
def save_workout_plan(plan: list):
    # """
    # IMPORTANTE: Única forma de guardar rutinas. LLAMA A ESTA HERRAMIENTA cuando el usuario acepte una rutina.
    # 'plan' debe ser una lista de uno o más días con: day_of_week (0-6), routine_name (str) y exercises (list).
    # """
    """
     IMPORTANTE: Única forma de guardar rutinas. LLAMA A ESTA HERRAMIENTA cuando el usuario acepte una rutina.
    'plan' debe ser una lista de uno o más días, cada día con:
    - day_of_week (int): 0-6
    - routine_name (str): Ejemplo 'Empuje'
    - exercises (list): Lista de objetos con:
        * name (str): Nombre del ejercicio
        * wger_id (int): ID de la API
        * description (str): Explicación técnica o series/reps
        * video_url (str): URL del video de ejecución
    """
    user = user_ctx.get()
    request = request_ctx.get()
    print(f"DEBUG TOOL: Intentando guardar rutina para {user.username}")
    
    try:
        results = []
        for day_data in plan:
            day = day_data.get('day_of_week', day_data.get('dayOfWeek'))
            name = day_data.get('routine_name', day_data.get('routineName', 'Rutina'))
            exercises = day_data.get('exercises', [])
            
            if day is None:
                print(f"DEBUG TOOL: Saltando bloque sin día: {day_data}")
                continue

            
            # Limpiar rutina previa
            Routine.objects.filter(user=user, day_of_week=day).delete()
            
            # Crear nueva rutina
            r = Routine.objects.create(user=user, day_of_week=day, name=name)
            
            for idx, ex in enumerate(exercises):
                if isinstance(ex, dict):
                    # Robust check for both Snake Case and Camel Case (from APIs)
                    ex_name = ex.get('name', 'Ejercicio')
                    wger_id = ex.get('wger_id')
                    desc = ex.get('description', ex.get('overview', ''))
                    video = ex.get('video_url', ex.get('videoUrl'))
                    image = ex.get('image_url', ex.get('imageUrl'))
                    # Advanced fields
                    primary = ex.get('primary_muscle', ex.get('primaryMuscle', ''))
                    secondary = ex.get('secondary_muscle', ex.get('secondaryMuscle', ''))
                    category = ex.get('category', '')
                    instructions = ex.get('instructions', '')
                    
                    # If instructions is a list (common in ExerciseDB), join it
                    if isinstance(instructions, list):
                        instructions = "\n".join(instructions)
                        
                    sets = ex.get('sets', [])
                else:
                    ex_name = str(ex)
                    wger_id = None
                    desc = ""
                    video = None
                    image = None
                    primary = ""
                    secondary = ""
                    category = ""
                    instructions = ""
                    sets = []

                RoutineExercise.objects.create(
                    routine=r,
                    wger_id=wger_id,
                    name=ex_name,
                    description=desc,
                    video_url=video,
                    image_url=image,
                    primary_muscle=primary,
                    secondary_muscle=secondary,
                    category=category,
                    instructions=instructions,
                    sets_data=sets,
                    order=idx
                )

            results.append(f"Día {day}")


        
        # Crear Notificación persistente
        msg = f"Tu plan de entrenamiento para {', '.join(results)} ha sido guardado correctamente."
        Notification.objects.create(
            user=user,
            message=msg,
            type=Notification.Type.SUCCESS
        )
        
        if request:
            messages.success(request, msg)
        
        return msg
    except Exception as e:
        return f"Error al guardar la rutina: {str(e)}"
