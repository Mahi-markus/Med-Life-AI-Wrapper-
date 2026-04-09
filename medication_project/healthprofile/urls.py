from django.urls import path
from .views import get_health_profile

urlpatterns = [
    path('profile/', get_health_profile),
]