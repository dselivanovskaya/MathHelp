from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from pages.views import IndexView, ReferenceView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('reference', ReferenceView.as_view(), name='reference'),

    path('admin/', admin.site.urls),

    path('tickets', include('tickets.urls')),
    path('forum/', include('forum.urls')),

    path('', include('accounts.urls')),
    path('', include('profiles.urls')),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
