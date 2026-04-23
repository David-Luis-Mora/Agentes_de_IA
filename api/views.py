from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from agent.factory import get_gym_agent
from django.contrib.auth.models import User
from core.models import UserProfile

class ChatView(APIView):
    def post(self, request):
        user_id = request.data.get('user_id') # In a real app, use request.user
        user_message = request.data.get('message')
        
        if not user_id or not user_message:
            return Response({"error": "Missing user_id or message"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        agent_executor = get_gym_agent()
        
        try:
            # We can use a simple chat history in memory for now or persist it in DB
            response = agent_executor.invoke({
                "input": user_message,
                "chat_history": [] # TODO: Implement history persistence
            })
            
            return Response({"response": response["output"]}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class UserProfileView(APIView):
    def get(self, request, user_id):
        try:
            profile = UserProfile.objects.get(user_id=user_id)
            return Response({
                "weight": profile.weight,
                "height": profile.height,
                "days_per_week": profile.days_per_week,
                "time_per_session": profile.time_per_session,
                "fitness_goal": profile.fitness_goal
            })
        except UserProfile.DoesNotExist:
            return Response({"error": "Profile not found"}, status=status.HTTP_404_NOT_FOUND)
