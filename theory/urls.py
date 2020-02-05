from django.urls import path

from .views import theory

urlpatterns = [
	path('', theory, name="theory"),
]

