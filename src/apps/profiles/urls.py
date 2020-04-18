from django.conf import settings
from django.urls import path

from .apps import ProfilesConfig
from .views import (ProfileDeleteView, ProfileRedirectView, ProfileUpdateView,
                    ProfileView)

urlpatterns = [
    path(
        'profiles/redirect',
        ProfileRedirectView.as_view(),
        name=settings.LOGIN_REDIRECT_URL
    ),
    path(
        '<slug:username>',
        ProfileView.as_view(),
        name=ProfilesConfig.PROFILE_URL
    ),
    path(
        '<slug:username>/edit',
        ProfileUpdateView.as_view(),
        name=ProfilesConfig.PROFILE_UPDATE_URL
    ),
    path(
        '<slug:username>/delete',
        ProfileDeleteView.as_view(),
        name=ProfilesConfig.PROFILE_DELETE_URL
    )
]
