from django.urls import include, path

from .views import show_user_profile, delete_user_profile, update_user_profile

urlpatterns = [
    path('<slug:username>', show_user_profile, name='show-user-profile'),
    path('<slug:username>/delete', delete_user_profile, name='delete-user-profile'),
    path('<slug:username>/update', update_user_profile, name='update-user-profile')
]