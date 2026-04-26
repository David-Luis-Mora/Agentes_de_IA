from langchain_core.tools import tool
from core.models import Profile
from django.contrib.auth.models import User

@tool
def get_user_profile(username: str):
    """
    Recupera el perfil de fitness del usuario, incluyendo peso, altura y disponibilidad.
    """
    try:
        user = User.objects.get(username=username)
        profile = user.profile
        return {
            "peso": profile.weight,
            "altura": profile.height,
            "dias_por_semana": profile.days_per_week,
            "tiempo_por_sesion": profile.time_per_session,
            "objetivo_fitness": profile.fitness_goal,
            "nivel_experiencia": profile.experience_level
        }
    except Exception as e:
        return f"Perfil de usuario no encontrado: {str(e)}"

@tool
def update_user_profile(username: str, **kwargs):
    """
    Actualiza el perfil de fitness del usuario.
    Campos disponibles: weight, height, days_per_week, time_per_session, fitness_goal, experience_level.
    """
    try:
        user = User.objects.get(username=username)
        profile = user.profile
        for key, value in kwargs.items():
            if hasattr(profile, key):
                setattr(profile, key, value)
        profile.save()
        return "Perfil actualizado con éxito."
    except Exception as e:
        return f"Error al actualizar el perfil: {str(e)}"
