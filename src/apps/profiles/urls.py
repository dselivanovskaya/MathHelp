from django.urls import path

from .apps import ProfilesConfig
from .views import ProfileRedirectView, ProfileDetailView, ProfileUpdateView


urlpatterns = [
    path(
        'redirect',
        ProfileRedirectView.as_view(),
        name=ProfilesConfig.PROFILE_REDIRECT_URL
    ),
    path(
        '<slug:username>',
        ProfileDetailView.as_view(),
        name=ProfilesConfig.PROFILE_DETAIL_URL
    ),
    path(
        '<slug:username>/update',
        ProfileUpdateView.as_view(),
        name=ProfilesConfig.PROFILE_UPDATE_URL
    ),
]
