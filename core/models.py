from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    weight = models.FloatField(help_text="Weight in kg", null=True, blank=True)
    height = models.FloatField(help_text="Height in cm", null=True, blank=True)
    days_per_week = models.IntegerField(default=3, help_text="Number of days the user can train per week")
    time_per_session = models.IntegerField(default=60, help_text="Minutes per session")
    fitness_goal = models.CharField(max_length=255, help_text="e.g., Hypertrophy, Weight Loss, Strength", default="Hypertrophy")
    experience_level = models.CharField(max_length=50, choices=[('Beginner', 'Beginner'), ('Intermediate', 'Intermediate'), ('Advanced', 'Advanced')], default='Beginner')

    def __str__(self):
        return f"{self.user.username}'s Profile"
