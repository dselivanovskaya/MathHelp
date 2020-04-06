from django.urls import include, path

from .views import get_user_profile, update_user_profile, delete_user_profile

urlpatterns = [
    path('', get_user_profile, name='user-profile'),
    path('delete/', delete_user_profile, name='delete-user-profile'),
    path('update/', update_user_profile, name='update-user-profile')
]
