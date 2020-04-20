from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path('', include('pages.urls')),
    path('admin/', admin.site.urls),

    path('tickets/', include('tickets.urls')),
    path('forum/', include('forum.urls')),

    path('accounts/', include('accounts.urls')),
    path('profiles/', include('profiles.urls')),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
