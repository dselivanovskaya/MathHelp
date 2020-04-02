from django.db import models


class Ticket(models.Model):

    name = models.CharField(blank=False, max_length=512)
    level = models.SmallIntegerField(blank=False)
    path = models.CharField(max_length=512, null=True, blank=True)
    slug = models.CharField(max_length=64, default='default')

    def __str__(self):
        return self.name
