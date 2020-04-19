import os

from django.conf import settings
from django.db import models


class Ticket(models.Model):

    name  = models.CharField(max_length=256)
    level = models.SmallIntegerField()
    filename = models.CharField(max_length=256)

    def __str__(self):
        return self.name

    def get_absolute_path(self):
        return os.path.join(settings.MEDIA_ROOT, 'tickets', self.filename)

    def get_absolute_url(self):
        return os.path.join(settings.MEDIA_URL, 'tickets', self.filename)
