from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic.base import TemplateView

urlpatterns = [
    # TODO move somewhere
    path('', TemplateView.as_view(template_name='index.html'), name='index'),
    path('additions', TemplateView.as_view(template_name='additions.html'),
                                                          name='additions'),

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
