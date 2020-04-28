from django.urls import path

from .apps import PagesConfig
from .views import IndexView, ReferenceView


urlpatterns = [
    path('', IndexView.as_view(), name=PagesConfig.INDEX_URL),
    path('references', ReferenceView.as_view(), name=PagesConfig.REFERENCES_URL),
]
