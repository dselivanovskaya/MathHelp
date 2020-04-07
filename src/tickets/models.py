import os

from django.db import models


class Ticket(models.Model):

    name  = models.CharField(max_length=256)
    level = models.SmallIntegerField()
    filename = models.CharField(max_length=256)

    def __str__(self):
        return self.name

    def get_absolute_path(self):
        return os.path.abspath(os.path.join('src/tickets/media', self.filename))
