from django.db import models

# Create your models here.

class Ticket(models.Model):
    name = models.CharField(blank=False, max_length=512)
    level = models.SmallIntegerField(blank=False)
    path = models.CharField(max_length=512, null=True, blank=True)

    def __str__(self):
        return self.name
