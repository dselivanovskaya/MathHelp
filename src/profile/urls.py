from django.urls import path

from .views import DeleteProfileView, ProfileView, UpdateProfileView

urlpatterns = [
    path('',        ProfileView.as_view(),       name='profile'),
    path('/update', UpdateProfileView.as_view(), name='update-profile'),
    path('/delete', DeleteProfileView.as_view(), name='delete-profile'),
]
