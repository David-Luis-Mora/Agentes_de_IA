from django.urls import path
from .views import ChatView, UserProfileView

urlpatterns = [
    path('chat/', ChatView.as_view(), name='chat'),
    path('profile/<int:user_id>/', UserProfileView.as_view(), name='profile-detail'),
]
