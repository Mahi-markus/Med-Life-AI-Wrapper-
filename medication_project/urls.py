from django.urls import path, include


urlpatterns = [
    path('api/medication/', include('medication.urls')),
      path('api/auth/', include('accounts.urls')),
    path('api/health/', include('healthprofile.urls')),
]
