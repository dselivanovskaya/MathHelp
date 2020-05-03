from django.test import TestCase

from tests.data import USER_MALE


class ProfilesSignalsTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = USER_MALE.create_in_db()

    def test_profile_is_created_when_user_is_created(self):
        self.assertTrue(self.user.profile)
