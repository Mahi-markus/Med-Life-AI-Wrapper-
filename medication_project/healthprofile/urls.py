from django.urls import path
from .views import get_health_profile, get_health_plan, get_dietary_recommendation

urlpatterns = [
    path('profile/', get_health_profile, name='get_health_profile'),
    path('plan/', get_health_plan, name='get_health_plan'),
    path('dietary-recommendation/', get_dietary_recommendation, name='get_dietary_recommendation'),
]