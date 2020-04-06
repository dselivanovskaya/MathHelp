from django.contrib.auth.models import User
from django.db import models

from .constants import FEMALE, GENDER_CHOICES, MALE


class Profile(models.Model):

    user   = models.OneToOneField(User, on_delete=models.CASCADE)
    gender = models.PositiveSmallIntegerField('gender', choices=GENDER_CHOICES, null=True)
    login_count = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username

    def __repr__(self):
        return (f"Profile(user={self.user}, "
                f"gender={self.gender}, "
                f"login_count={self.login_count})")
