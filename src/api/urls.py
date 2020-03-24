from django.urls import path, include

from .views import ListUsersView

urlpatterns = [
    path('users/', ListUsersView.as_view(), name='users-all'),
]
