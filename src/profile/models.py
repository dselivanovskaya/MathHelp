from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):

    MALE, FEMALE = 'M', 'F'
    GENDER_CHOICES = ((MALE, 'Male'), (FEMALE, 'Female'))

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default=MALE)
    age = models.PositiveSmallIntegerField(default=0)

    image = models.ImageField(upload_to='photos', default='photos/default-avatar.jpg')
    login_count = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username

    def __repr__(self):
        return (f"Profile(user={self.user}, "
                f"gender={self.gender}, "
                f"age={self.age}, "
                f"login_count={self.login_count})")

    def is_male(self):
        return self.gender == self.MALE

    def is_female(self):
        return self.gender == self.FEMALE


@receiver(post_save, sender=User)
def create_user_profile(instance, created, **kwargs):
    ''' For every new registered user (created User) create a Profile. '''
    if created:
        Profile.objects.create(user=instance).save()
