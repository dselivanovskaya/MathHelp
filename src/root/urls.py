from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import include, path
from django.views.generic.base import TemplateView


urlpatterns = [

    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('additions', TemplateView.as_view(template_name='additions.html'),
                                                          name='additions'),

    path('', include('accounts.urls')),

    path('admin/', admin.site.urls),

    path('profiles', include('profiles.urls')),
    path('tickets', include('tickets.urls')),
    path('forum/', include('forum.urls')),

]

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
