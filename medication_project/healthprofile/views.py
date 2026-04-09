from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import healthProfile

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_health_profile(request):
    profile = healthProfile.objects.get(patient=request.user)

    return Response({
        "age": profile.age,
        "bmi": profile.bmi
    })