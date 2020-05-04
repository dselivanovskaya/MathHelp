from django.test import TestCase

from tests.data import MALE_USER


class ProfilesSignalsTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = MALE_USER.create()

    def test_profile_is_created_when_user_is_created(self):
        self.assertTrue(self.user.profile)
