from django.db import models
from django.contrib.auth.models import User

from .constants import MALE, FEMALE


class Profile(models.Model):

    GENDER_CHOICES = ((MALE, 'Male'), (FEMALE, 'Female'))

    user   = models.OneToOneField(User, on_delete=models.CASCADE)
    gender = models.PositiveSmallIntegerField('gender', choices=GENDER_CHOICES,
                                              blank=True, null=True)
    login_count = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.user}'

    def __repr__(self):
        return (f'Profile(user={self.user}, gender={self.gender}, '
               f'login_count={self.login_count})')
