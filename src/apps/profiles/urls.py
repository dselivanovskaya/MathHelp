from django.urls import path

from .views import (
    ProfileRedirectView, ProfileView, ProfileUpdateView, ProfileDeleteView
)

urlpatterns = [
    path(
        'profiles/redirect',
        ProfileRedirectView.as_view(),
        name=ProfileRedirectView.url_name
    ),
    path(
        '<slug:username>',
        ProfileView.as_view(),
        name=ProfileView.url_name
    ),
    path(
        '<slug:username>/edit',
        ProfileUpdateView.as_view(),
        name=ProfileUpdateView.url_name
    ),
    path(
        '<slug:username>/delete',
        ProfileDeleteView.as_view(),
        name=ProfileDeleteView.url_name
    )
]
