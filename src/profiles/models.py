import os

from django.contrib.auth.models import User
from django.db import models

from django.conf import settings


class Profile(models.Model):

    MALE, FEMALE = 1, 2
    GENDER_CHOICES = ((MALE, 'Male'), (FEMALE, 'Female'))

    user   = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(
        upload_to='photos',
        default='photos/default-avatar.jpg',
    )
    age = models.PositiveSmallIntegerField(default = 0)
    first_name = models.CharField(default = '', max_length = 64)
    last_name = models.CharField(default = '', max_length = 64)
    gender = models.PositiveSmallIntegerField('gender', choices=GENDER_CHOICES, null=True)
    login_count = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username

    def __repr__(self):
        return (f"Profile(user={self.user}, "
                f"gender={self.gender}, "
                f"login_count={self.login_count})")
