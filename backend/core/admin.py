from django.contrib import admin
from .models import Profile, Routine, RoutineExercise, Notification, Token

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'nickname', 'fitness_goal', 'experience_level', 'role')
    search_fields = ('user__username', 'nickname', 'email')
    list_filter = ('role', 'fitness_goal')

class RoutineExerciseInline(admin.StackedInline):
    model = RoutineExercise
    extra = 1
    fields = (
        'name', 'order', 'wger_id', 'category', 
        'primary_muscle', 'secondary_muscle', 
        'description', 'instructions', 
        'video_url', 'image_url', 'sets_data'
    )


@admin.register(Routine)
class RoutineAdmin(admin.ModelAdmin):
    list_display = ('user', 'day_of_week', 'name', 'created_at')
    list_filter = ('day_of_week', 'user')
    search_fields = ('name', 'user__username')
    inlines = [RoutineExerciseInline]

@admin.register(RoutineExercise)
class RoutineExerciseAdmin(admin.ModelAdmin):
    list_display = ('name', 'routine', 'primary_muscle', 'category', 'order')
    list_filter = ('routine__user', 'category')
    search_fields = ('name', 'primary_muscle')


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'message', 'type', 'created_at', 'is_read')
    list_filter = ('type', 'is_read', 'user')
    search_fields = ('message', 'user__username')

@admin.register(Token)
class TokenAdmin(admin.ModelAdmin):
    list_display = ('user', 'key', 'created_at')
    readonly_fields = ('key', 'created_at')
