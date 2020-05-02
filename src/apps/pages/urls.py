from django.urls import path

from .apps import PagesConfig
from .views import IndexView, ReferencesView


urlpatterns = [
    path('', IndexView.as_view(), name=PagesConfig.INDEX_URL),
    path('references', ReferencesView.as_view(), name=PagesConfig.REFERENCES_URL),
]
