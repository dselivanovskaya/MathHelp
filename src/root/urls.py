from django.contrib import admin
from django.urls import include, path
from django.views.generic.base import TemplateView
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [

    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('additions', TemplateView.as_view(template_name='additions.html'),
                                                          name='additions'),

    path('', include('authentication.urls')),
    path('', include('registration.urls')),

    path('admin', admin.site.urls),
    path('api/', include('api.urls')),

    path('profile', include('profile.urls')),
    path('tickets/', include('tickets.urls')),

]

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
