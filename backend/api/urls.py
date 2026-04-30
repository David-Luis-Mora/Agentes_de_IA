from django.urls import path
from .views import chat, profile, register, get_routines, notifications
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('chat/', chat, name='chat'),
    path('profile/', profile, name='profile'),
    path('routines/', get_routines, name='routines'),
    path('notifications/', notifications, name='notifications'),
]
