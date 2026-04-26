import json
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework_simplejwt.tokens import RefreshToken
from langchain_core.messages import HumanMessage

from core.models import Profile, Token, Routine

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_routines(request):
    routines = Routine.objects.filter(user=request.user).prefetch_related('exercises')
    data = {}
    for r in routines:
        data[r.day_of_week] = {
            "name": r.name,
            "exercises": [
                {
                    "name": ex.name,
                    "description": ex.description,
                    "video_url": ex.video_url,
                    "image_url": ex.image_url,
                    "order": ex.order
                } for ex in r.exercises.all().order_by('order')
            ]
        }
    return JsonResponse(data)
from agent.factory import get_gym_agent

@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def register(request):
    data = request.data
    username = data.get('username')
    password = data.get('password')
    email = data.get('email', '')

    if not username or not password:
        return JsonResponse({"error": "Username and password required"}, status=400)

    if User.objects.filter(username=username).exists():
        return JsonResponse({"error": "Username already exists"}, status=400)

    user = User.objects.create_user(username=username, password=password, email=email)
    # Create profile automatically (Profile is the new model name)
    Profile.objects.create(user=user, email=email, nickname=username)
    
    refresh = RefreshToken.for_user(user)
    return JsonResponse({
        "user_id": user.id,
        "username": user.username,
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }, status=201)

import asyncio

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def chat(request):
    user = request.user
    user_message = request.data.get('message')
    
    if not user_message:
        return JsonResponse({"error": "Missing message"}, status=400)

    try:
        # Since @api_view might not handle async functions correctly in this environment,
        # we run the async agent logic in a sync wrapper.
        async def call_agent():
            agent = await get_gym_agent(user)
            response = await agent.ainvoke({
                "messages": [
                    HumanMessage(content=user_message)
                ]
            })
            return response["messages"][-1].content

        output = asyncio.run(call_agent())
        return JsonResponse({"response": output}, status=200)
    except Exception as e:
        print(f"Error in chat view: {e}")
        import traceback
        traceback.print_exc()
        return JsonResponse({"error": str(e)}, status=500)

@api_view(['GET', 'PUT'])
@permission_classes([permissions.IsAuthenticated])
def profile(request):
    try:
        user_profile = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        return JsonResponse({"error": "Profile not found"}, status=404)

    if request.method == 'GET':
        return JsonResponse({
            "username": request.user.username,
            "name": user_profile.name,
            "nickname": user_profile.nickname,
            "email": user_profile.email,
            "weight": user_profile.weight,
            "height": user_profile.height,
            "days_per_week": user_profile.days_per_week,
            "time_per_session": user_profile.time_per_session,
            "fitness_goal": user_profile.fitness_goal,
            "experience_level": user_profile.experience_level,
            "country": user_profile.country,
            "balance": user_profile.balance,
            "bio": user_profile.bio
        })

    if request.method == 'PUT':
        data = request.data
        user_profile.name = data.get('name', user_profile.name)
        user_profile.nickname = data.get('nickname', user_profile.nickname)
        user_profile.email = data.get('email', user_profile.email)
        user_profile.weight = data.get('weight', user_profile.weight)
        user_profile.height = data.get('height', user_profile.height)
        user_profile.days_per_week = data.get('days_per_week', user_profile.days_per_week)
        user_profile.time_per_session = data.get('time_per_session', user_profile.time_per_session)
        user_profile.fitness_goal = data.get('fitness_goal', user_profile.fitness_goal)
        user_profile.experience_level = data.get('experience_level', user_profile.experience_level)
        user_profile.country = data.get('country', user_profile.country)
        user_profile.phone = data.get('phone', user_profile.phone)
        user_profile.bio = data.get('bio', user_profile.bio)
        user_profile.address = data.get('address', user_profile.address)
        user_profile.balance = data.get('balance', user_profile.balance)
        user_profile.save()
        return JsonResponse({"message": "Profile updated successfully"})
