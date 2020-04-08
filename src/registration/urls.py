from django.urls import path

from .views import sign_up, get_username_status

urlpatterns = [
    path('sign-up', sign_up, name='sign-up'),
    path('username-status', get_username_status, name='username-status'),
]
