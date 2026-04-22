from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from medication.models import Patient
from rest_framework_simplejwt.views import TokenRefreshView
User = get_user_model()



@api_view(['POST'])
def register(request):
    username = request.data.get("username")
    password = request.data.get("password")
    name = request.data.get("name")

    if User.objects.filter(username=username).exists():
        return Response({"error": "Username already exists"}, status=400)

    user = User.objects.create_user(username=username, password=password)

    # create patient automatically
    Patient.objects.create(user=user, name=name)

    return Response({"message": "User registered successfully"})


from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

@api_view(['POST'])
def login(request):
    username = request.data.get("username")
    password = request.data.get("password")

    user = authenticate(username=username, password=password)

    if user is None:
        return Response({"error": "Invalid credentials"}, status=400)

    refresh = RefreshToken.for_user(user)

    return Response({
        "access": str(refresh.access_token),
        "refresh": str(refresh),
    })