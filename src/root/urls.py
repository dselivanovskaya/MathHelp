from django.contrib import admin
from django.urls import include, path
from django.views.generic.base import TemplateView


urlpatterns = [

    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('', include('profiles.urls')),  # TODO

    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('', include('authentication.urls')),

    path('additions/', TemplateView.as_view(template_name='additions.html'),
                                                          name='additions'),
    path('register/', include('registration.urls')),
    path('tickets/', include('tickets.urls')),
]
