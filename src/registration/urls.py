from django.urls import path, include

from .views import register_user

urlpatterns = [
    path('', register_user, name='register'),
]
