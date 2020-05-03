import os

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse

from .apps import ProfilesConfig


def get_photo_upload_path(instance, filename):
    ''' Profile photo will be uploaded to this path. '''
    return os.path.join('profiles', str(instance.user.id), 'photos', filename)


class Profile(models.Model):

    error_messages = {
        'invalid_delete_photo': 'Can not delete default photo.',
    }

    PHOTO_MAX_WIDTH, PHOTO_MAX_HEIGHT = 250, 250
    DEFAULT_PHOTO_PATH = os.path.join('profiles', 'default-avatar.jpg')
    MALE, FEMALE = 'M', 'F'
    GENDER_CHOICES = ((MALE, 'Male'), (FEMALE, 'Female'))

    @staticmethod
    def get_max_photo_size_display():
        return f'{Profile.PHOTO_MAX_WIDTH} x {Profile.PHOTO_MAX_HEIGHT}'

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

    def __str__(self):
        return self.user.username

    def __repr__(self):
        return (
            f"{self.__class__.__name__}(first_name='{self.first_name}', "
            f"last_name='{self.last_name}', photo='{self.photo}', "
            f"gender='{self.gender}', age={self.age})"
        )

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
        return self.photo == self.DEFAULT_PHOTO_PATH

    def has_uploaded_photo(self):
        return self.photo != self.DEFAULT_PHOTO_PATH

    def delete_photo(self):
        if self.has_default_photo():
            raise ValidationError(self.error_messages['invalid_delete_photo'])
        try:
            os.remove(self.photo.path)
        except FileNotFoundError as e:
            print(e)
