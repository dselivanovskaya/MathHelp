from django.db import models
from django.db.models.signals import pre_save, post_save

from django.dispatch import receiver
from django.contrib.auth.models import User

from .constants import MALE, FEMALE, GENDER_CHOICES


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
    ''' Automatically create Profile for every new User. '''
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(instance, **kwargs):
    ''' Save automatically created Profile. '''
    instance.profile.save()
