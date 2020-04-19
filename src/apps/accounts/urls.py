from django.conf import settings
from django.urls import path

from .views import SigninView, SignoutView, SignupView

urlpatterns = [
    path('signin',  SigninView.as_view(),  name=settings.LOGIN_URL),
    path('signup',  SignupView.as_view(),  name=settings.REGISTER_URL),
    path('signout', SignoutView.as_view(), name=settings.LOGOUT_URL),
]
