from django.urls import path
from .views import process_prescription

urlpatterns = [
    path('upload-prescription/', process_prescription, name='upload-prescription'),
]
