from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse

from tests.data import MALE_USER

from profiles.apps import ProfilesConfig


class ProfileModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = MALE_USER.create()
        cls.instance = cls.user.profile

    def test_str(self):
        self.assertEquals(str(self.instance), self.instance.user.username)

    def test_get_absolute_url(self):
        url = reverse(ProfilesConfig.PROFILE_DETAIL_URL, args=[self.user.username])
        self.assertEquals(self.instance.get_absolute_url(), url)

    def test_get_absolute_update_url(self):
        url = reverse(ProfilesConfig.PROFILE_UPDATE_URL, args=[self.user.username])
        self.assertEquals(self.instance.get_absolute_update_url(), url)

    def test_get_full_name(self):
        string = f'{self.instance.first_name} {self.instance.last_name}'
        self.assertEquals(self.profile.get_full_name(), string)

    def test_is_male_is_female(self):
        self.assertTrue(self.instance.is_male())
        self.assertFalse(self.instance.is_female())

    def test_has_default_uploaded_photo(self):
        self.assertTrue(self.instance.has_default_photo())
        self.assertFalse(self.instance.has_uploaded_photo())

    def test_delete_photo(self):
        with self.assertRaises(ValidationError):
            self.instance.delete_photo()

    def test_get_max_photo_size_display(self):
        string = f'{self.instance.PHOTO_MAX_WIDTH} x {self.instance.PHOTO_MAX_HEIGHT}'
        self.assertEquals(self.instance.get_max_photo_size_display(), string)
