from django.urls import include, path

from .views import ListUsersView

urlpatterns = [
    path('users', ListUsersView.as_view()),
]
