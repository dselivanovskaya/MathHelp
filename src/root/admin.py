from django.contrib import admin
from django.contrib.auth.models import Group


admin.site.site_header = 'MathHelp administration'
admin.site.unregister(Group)
