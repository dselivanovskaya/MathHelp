from django.urls import path

from .apps import PagesConfig as pages_config
from .views import IndexView, ReferenceView

urlpatterns = [
    path('', IndexView.as_view(), name=pages_config.INDEX_URL),
    path('reference', ReferenceView.as_view(), name=pages_config.REFERENCE_URL),
]
