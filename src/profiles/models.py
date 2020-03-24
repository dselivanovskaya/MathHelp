from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

class Profile(models.Model):

    GENDER_CHOICES = (
        (1, 'Male'),
        (2, 'Female'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)  
    gender = models.PositiveSmallIntegerField('gender',
                                              choices=GENDER_CHOICES,
                                              blank=True,
                                              null=True)

    def __str__(self):  
          return f"{self.user}'s profile"

