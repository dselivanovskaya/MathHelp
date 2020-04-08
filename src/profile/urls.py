from django.urls import include, path

from .views import get_profile, update_profile, delete_profile

urlpatterns = [
    path('', get_profile, name='profile'),
    path('/update', update_profile, name='update-profile'),
    path('/delete', delete_profile, name='delete-profile'),
]
