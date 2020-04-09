from django.urls import path

from .views import ProfileView, EditProfileView, DeleteProfileView

urlpatterns = [
    path('',        ProfileView.as_view(),       name='profile'),
    path('/edit',   EditProfileView.as_view(),   name='edit-profile'),
    path('/delete', DeleteProfileView.as_view(), name='delete-profile'),
]
