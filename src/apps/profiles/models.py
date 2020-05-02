import os

from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse

from .apps import ProfilesConfig


def get_profile_photo_upload_path(profile, filename):
    ''' Custom folder for every user. '''
    return os.path.join('profiles', str(profile.user.id), 'photos', filename)


def get_default_profile_photo_path():
    ''' Default profile photo. '''
    return os.path.join('profiles', 'default-avatar.jpg')


class Profile(models.Model):

    MALE, FEMALE = 'M', 'F'
    GENDER_CHOICES = ((MALE, 'Male'), (FEMALE, 'Female'))

    PHOTO_MAX_WIDTH = 250
    PHOTO_MAX_HEIGHT = 250

    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    first_name = models.CharField(max_length=128, default='')
    last_name = models.CharField(max_length=128, default='')
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

    def get_absolute_url(self):
        return reverse(ProfilesConfig.PROFILE_DETAIL_URL, args=[self.user.username])

    def get_absolute_update_url(self):
        return reverse(ProfilesConfig.PROFILE_UPDATE_URL, args=[self.user.username])

    def is_male(self):
        return self.gender == self.MALE

    def is_female(self):
        return self.gender == self.FEMALE

    def has_default_photo(self):
        ''' Check if user's profile photo is default. '''
        return self.photo.path == get_default_profile_photo_path()

    def has_uploaded_photo(self):
        ''' Check if user's profile photo is uploaded. '''
        return self.photo.path != get_default_profile_photo_path()

    def delete_photo(self):
        ''' Delete user's profile photo. '''
        try:
            os.remove(self.photo.path)
        except FileNotFoundError as e:
            print(e)
