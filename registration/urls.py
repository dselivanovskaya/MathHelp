from django.urls import path, include

from .views import register, ListUsersView

urlpatterns = [
    path('', register, name='register'),
    path('users/', ListUsersView.as_view(), name='users-all'),
]
