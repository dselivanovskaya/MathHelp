from django.urls import path

from .views import ProfileView, ProfileUpdateView, ProfileDeleteView

urlpatterns = [
    path('<slug:username>', ProfileView.as_view(), name=ProfileView.url_name),
    path('<slug:username>/edit', ProfileUpdateView.as_view(), name=ProfileUpdateView.url_name),
    path('<slug:username>/delete', ProfileDeleteView.as_view(), name=ProfileDeleteView.url_name),
]
