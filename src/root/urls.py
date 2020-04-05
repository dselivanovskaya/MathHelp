from django.contrib import admin
from django.urls import include, path
from django.views.generic.base import TemplateView

from .views import login_user, logout_user

urlpatterns = [

    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('', include('profiles.urls')),  # TODO

    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),  # <-- REST api

    path('login/',  login_user,  name='login'),
    path('logout/', logout_user, name='logout'),

    path('additions/', TemplateView.as_view(template_name='additions.html'),
                                                          name='additions'),
    path('register/', include('registration.urls')),
    path('tickets/', include('tickets.urls')),
]
