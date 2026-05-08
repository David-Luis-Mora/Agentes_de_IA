import uuid
from django.db import models
from django.conf import settings

class Token(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='tokens', on_delete=models.CASCADE
    )
    key = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Token for {self.user.username}"

class Profile(models.Model):
    class Role(models.IntegerChoices):
        USER = 1, 'Usuario'
        MODERATOR = 2, 'Moderador'
        ADMIN = 3, 'Administrador'

    role = models.PositiveSmallIntegerField(choices=Role.choices, default=Role.USER)
    
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile'
    )
    
    # Information fields
    name = models.CharField(max_length=255, blank=True)
    nickname = models.CharField(max_length=255, blank=True)
    email = models.CharField(max_length=255, blank=True)
    
    # Fitness & Profile data
    weight = models.FloatField(help_text="Weight in kg", null=True, blank=True)
    height = models.FloatField(help_text="Height in cm", null=True, blank=True)
    days_per_week = models.IntegerField(default=3)
    time_per_session = models.IntegerField(default=60)
    fitness_goal = models.CharField(max_length=255, default="Hypertrophy")
    experience_level = models.CharField(max_length=50, default='Beginner')
    
    # Extra fields from reference
    country = models.CharField(max_length=255, blank=True)
    balance = models.IntegerField(default=0)
    address = models.TextField(blank=True)
    phone = models.CharField(max_length=255, blank=True)
    bio = models.TextField(blank=True)
    avatar_url = models.URLField(blank=True, null=True, help_text='URL de un avatar remoto')
    avatar_file = models.ImageField(
        upload_to='avatars/', blank=True, null=True, help_text='Imagen subida por el usuario'
    )

    def __str__(self):
        return self.user.username

class Routine(models.Model):
    DAYS_OF_WEEK = [
        (0, 'Lunes'),
        (1, 'Martes'),
        (2, 'Miércoles'),
        (3, 'Jueves'),
        (4, 'Viernes'),
        (5, 'Sábado'),
        (6, 'Domingo'),
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='routines')
    day_of_week = models.IntegerField(choices=DAYS_OF_WEEK)
    name = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.get_day_of_week_display()}"

class RoutineExercise(models.Model):
    routine = models.ForeignKey(Routine, on_delete=models.CASCADE, related_name='exercises')
    wger_id = models.IntegerField(null=True, blank=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    video_url = models.URLField(blank=True, null=True)
    image_url = models.URLField(blank=True, null=True)
    
    # Advanced fields for professional display
    primary_muscle = models.CharField(max_length=255, blank=True)
    secondary_muscle = models.CharField(max_length=255, blank=True)
    category = models.CharField(max_length=255, blank=True)
    instructions = models.TextField(blank=True)
    sets_data = models.JSONField(default=list, blank=True) # stores [{reps: 12, weight: 20}, ...]
    
    order = models.PositiveIntegerField(default=0)


    def __str__(self):
        return f"{self.name} in {self.routine}"

class Notification(models.Model):
    class Type(models.TextChoices):
        SUCCESS = 'success', 'Éxito'
        INFO = 'info', 'Información'
        WARNING = 'warning', 'Advertencia'
        ERROR = 'error', 'Error'

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    type = models.CharField(max_length=20, choices=Type.choices, default=Type.INFO)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification for {self.user.username}: {self.message[:20]}..."
