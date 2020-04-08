from django.urls import path

from .views import sign_in, sign_out

urlpatterns = [
    path('sign-in', sign_in, name='sign-in'),
    path('sign-out', sign_out, name='sign-out'),
]
