from django.test import TestCase
from django.urls import reverse

from tests.data import USER_MALE

from profiles.apps import ProfilesConfig
from profiles.models import Profile


class ProfileModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = USER_MALE.create_in_db()
        cls.profile = cls.user.profile

    def test_get_absolute_url(self):
        self.assertEquals(
            self.profile.get_absolute_url(),
            reverse(ProfilesConfig.PROFILE_DETAIL_URL, args=[self.user.username])
        )

    def test_get_absolute_update_url(self):
        self.assertEquals(
            self.profile.get_absolute_update_url(),
            reverse(ProfilesConfig.PROFILE_UPDATE_URL, args=[self.user.username])
        )

    def test_get_full_name(self):
        self.assertEquals(self.profile.get_full_name(),
            f'{self.profile.first_name} {self.profile.last_name}'
        )

    def test_is_male_is_female(self):
        self.assertTrue(self.profile.is_male())
        self.assertFalse(self.profile.is_female())

    def test_has_default_uploaded_photo(self):
        self.assertTrue(self.profile.has_default_photo())
        self.assertFalse(self.profile.has_uploaded_photo())
