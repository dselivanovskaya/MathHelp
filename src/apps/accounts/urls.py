from django.urls import path

from .views import SigninView, SignupView, SignoutView

urlpatterns = [
    path('signin',  SigninView.as_view(),  name=SigninView.url_name),
    path('signup',  SignupView.as_view(),  name=SignupView.url_name),
    path('signout', SignoutView.as_view(), name=SignoutView.url_name),
]
