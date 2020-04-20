import os

from django.contrib.auth.models import User
from django.db import models


def get_profile_photo_upload_path(profile, filename):
    ''' Custom folder for every user. '''
    return os.path.join('profiles', profile.user.username, 'photos', filename)


def get_default_profile_photo_path():
    ''' Default profile photo. '''
    return os.path.join('profiles', 'default-avatar.jpg')


class Profile(models.Model):

    MALE, FEMALE = 'M', 'F'
    GENDER_CHOICES = ((MALE, 'Male'), (FEMALE, 'Female'))

    PHOTO_MAX_WIDTH = 250
    PHOTO_MAX_HEIGHT = 250

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.ImageField(
        upload_to=get_profile_photo_upload_path,
        default=get_default_profile_photo_path
    )
    gender = models.CharField(
        max_length=1, choices=GENDER_CHOICES, default=MALE, blank=True
    )
    age = models.PositiveSmallIntegerField(default=0, blank=True)
    login_count = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username

    # def has_default_photo(self):
    #     ''' Check if user's profile photo is default. '''
    #     return self.photo.path == get_default_profile_photo_path()

    def delete_photo(self):
        ''' Delete user's profile photo. '''
        try:
            os.remove(self.photo.path)
        except FileNotFoundError as err:
            print(err)

    def is_male(self):
        return self.gender == self.MALE

    def is_female(self):
        return self.gender == self.FEMALE
