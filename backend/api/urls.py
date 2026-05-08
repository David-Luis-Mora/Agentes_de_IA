from django.urls import path
from .views import chat, chat_history, profile, register, get_routines, get_exercise_detail, notifications
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('chat/', chat, name='chat'),
    path('chat-history/', chat_history, name='chat_history'),
    path('profile/', profile, name='profile'),
    path('routines/', get_routines, name='routines'),
    path('exercise/<int:exercise_id>/', get_exercise_detail, name='exercise_detail'),
    path('notifications/', notifications, name='notifications'),
]
