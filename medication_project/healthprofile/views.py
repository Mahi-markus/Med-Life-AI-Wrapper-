from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ValidationError
from .models import healthProfile, HealthPlan, DietaryRecommendation
from medication.models import Patient
from healthprofile.utils import generate_health_plan, generate_dietry_recommendation
import requests
# ...existing code...

@api_view(['GET', 'POST', 'PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def get_health_profile(request):
    # ensure Patient exists
    patient, _ = Patient.objects.get_or_create(user=request.user, defaults={'name': request.user.username})

    if request.method == 'GET':
        profile, created = healthProfile.objects.get_or_create(
            user=request.user,
            patient=patient,
            defaults={'age': 10, 'weight': 59, 'height_feet': 5, 'height_inches': 2, 'disease': 'humanity'}
        )
        return Response({
            "age": profile.age,
            "bmi": profile.bmi,
            "created": created
        })

    # For POST/PUT/PATCH accept fields from request body
    payload = request.data if isinstance(request.data, dict) else {}
    allowed = ['age', 'weight', 'height_feet', 'height_inches', 'disease', 'addition_info']
    data = {k: payload[k] for k in allowed if k in payload}

    if not data:
        return Response({"detail": "No valid fields provided"}, status=status.HTTP_400_BAD_REQUEST)

    profile, created = healthProfile.objects.get_or_create(
        user=request.user,
        patient=patient,
        defaults=data
    )

    if not created:
        # update existing
        for k, v in data.items():
            setattr(profile, k, v)
    try:
        profile.save()
    except ValidationError as exc:
        details = exc.message_dict if hasattr(exc, 'message_dict') else exc.messages
        return Response({"detail": details}, status=status.HTTP_400_BAD_REQUEST)

    # Generate HealthPlan after profile save
    try:
        plan_data = generate_health_plan(profile)
        HealthPlan.objects.create(
            patient=patient,
            food_chart=plan_data['food_chart'],
            exercise_plan=plan_data['exercise_plan'],
            sleep_plan=plan_data.get('sleep_plan', '')
        )
        dietary_data = generate_dietry_recommendation(profile)
        DietaryRecommendation.objects.create(
            patient=patient,
            breakfast=dietary_data.get('breakfast', ''),
            lunch=dietary_data.get('lunch', ''),
            dinner=dietary_data.get('dinner', ''),
            snacks=dietary_data.get('snacks', ''),
            foods_to_avoid=dietary_data.get('foods_to_avoid', '')
        ) 


    # generate diet and exercise plan 
        # diet_food_data =
    except Exception as e:
        # Log error but don't fail the request
        print(f"Failed to generate health plan: {e}")

    return Response({
        "age": profile.age,
        "bmi": profile.bmi,
        "created": created
    }, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)

    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_health_plan(request):
    from medication.models import Patient
    patient = Patient.objects.get(user=request.user)
    plan = HealthPlan.objects.filter(patient=patient).latest('generated_at')
    return Response({
        "food_chart": plan.food_chart,
        "exercise_plan": plan.exercise_plan,
        "sleep_plan": plan.sleep_plan,
        "generated_at": plan.generated_at
    })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_dietary_recommendation(request):
    from medication.models import Patient
    patient = Patient.objects.get(user=request.user)
    recommendation = DietaryRecommendation.objects.filter(patient=patient).latest('created_at')
    return Response({
        "breakfast": recommendation.breakfast,
        "lunch": recommendation.lunch,
        "dinner": recommendation.dinner,
        "snacks": recommendation.snacks,
        "foods_to_avoid": recommendation.food_to_avoid,
        "created_at": recommendation.created_at
    })