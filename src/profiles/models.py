from django.contrib.auth.models import User
from django.contrib.auth.signals import user_logged_in
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from .constants import FEMALE, GENDER_CHOICES, MALE


class Profile(models.Model):

    user   = models.OneToOneField(User, on_delete=models.CASCADE)
    gender = models.PositiveSmallIntegerField('gender', choices=GENDER_CHOICES, null=True)
    login_count = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username

    def __repr__(self):
        return (f"Profile(user={self.user}, "
                f"gender={'Male' if self.gender == MALE else 'Female'}, "
                f"login_count={self.login_count})")


@receiver(post_save, sender=User)
def create_user_profile(instance, created, **kwargs):
    ''' For every created User create a Profile. '''
    if created:
        Profile.objects.create(user=instance).save()
