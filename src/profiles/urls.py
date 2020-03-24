from django.urls import include, path

from django.views.generic.base import TemplateView

from .views import show_user_profile

urlpatterns = [
    path('', show_user_profile, name="show-user-profile"),
]
