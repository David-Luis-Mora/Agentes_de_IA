import os
import django
from langchain_core.tools import tool

# Setup Django before importing models
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gym_assistant.settings')
django.setup()

from core.models import UserProfile
from django.contrib.auth.models import User

@tool
def get_user_profile(username: str):
    """
    Retrieves the user's fitness profile including weight, height, and availability.
    """
    try:
        user = User.objects.get(username=username)
        profile = user.profile
        return {
            "weight": profile.weight,
            "height": profile.height,
            "days_per_week": profile.days_per_week,
            "time_per_session": profile.time_per_session,
            "fitness_goal": profile.fitness_goal,
            "experience_level": profile.experience_level
        }
    except Exception as e:
        return f"User profile not found: {str(e)}"

@tool
def update_user_profile(username: str, **kwargs):
    """
    Updates the user's fitness profile.
    Available fields: weight, height, days_per_week, time_per_session, fitness_goal, experience_level.
    """
    try:
        user = User.objects.get(username=username)
        profile = user.profile
        for key, value in kwargs.items():
            if hasattr(profile, key):
                setattr(profile, key, value)
        profile.save()
        return "Profile updated successfully."
    except Exception as e:
        return f"Error updating profile: {str(e)}"
