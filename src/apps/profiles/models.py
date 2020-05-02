import os

from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse

from .apps import ProfilesConfig


class Profile(models.Model):

    # Constants
    PHOTO_MAX_WIDTH, PHOTO_MAX_HEIGHT = 250, 250
    DEFAULT_PHOTO_PATH =  os.path.join('profiles', 'default-avatar.jpg')
    MALE, FEMALE = 'M', 'F'
    GENDER_CHOICES = ((MALE, 'Male'), (FEMALE, 'Female'))

    # Helper function.
    def get_photo_upload_path(profile, filename):
        return os.path.join('profiles', str(profile.user.id), 'photos', filename)

    # Fields
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    first_name = models.CharField(max_length=128, default='', blank=True)
    last_name = models.CharField(max_length=128, default='', blank=True)
    photo = models.ImageField(
        upload_to=get_photo_upload_path, default=DEFAULT_PHOTO_PATH
    )
    gender = models.CharField(
        max_length=1, choices=GENDER_CHOICES, default=MALE, blank=True
    )
    age = models.PositiveSmallIntegerField(default=0, blank=True)
    login_count = models.IntegerField(default=0)

    # Python methods
    def __str__(self):
        return self.user.username

    def __repr__(self):
        return (
            f'Profile(first_name={self.first_name}, last_name={self.last_name}, '
            f'photo={self.photo}, gender={self.gender}, age={self.age})'
        )

    # Custom methods
    def get_absolute_url(self):
        return reverse(ProfilesConfig.PROFILE_DETAIL_URL, args=[self.user.username])

    def get_absolute_update_url(self):
        return reverse(ProfilesConfig.PROFILE_UPDATE_URL, args=[self.user.username])

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'

    def is_male(self):
        return self.gender == self.MALE

    def is_female(self):
        return self.gender == self.FEMALE

    def has_default_photo(self):
        return self.photo == Profile.DEFAULT_PHOTO_PATH

    def has_uploaded_photo(self):
        return self.photo != Profile.DEFAULT_PHOTO_PATH

    # TODO Something bus me in here.
    def delete_photo(self):
        ''' Delete user's profile photo. '''
        try:
            os.remove(self.photo.path)
        except FileNotFoundError as e:
            print(e)
