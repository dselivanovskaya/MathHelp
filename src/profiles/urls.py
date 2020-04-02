from django.urls import include, path

from .views import show_user_profile

urlpatterns = [
    path('', show_user_profile, name="show-user-profile"),
]
