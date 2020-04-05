import os

from django.db import models


class Ticket(models.Model):

    name  = models.CharField(blank=False, max_length=256)
    level = models.SmallIntegerField(blank=False)
    path  = models.CharField(max_length=256, null=True, blank=False)
    slug  = models.CharField(max_length=64, default='default')

    def __str__(self):
        return self.name

    def get_absolute_path(self):
        return os.path.abspath(os.path.join('src/tickets', self.path))
