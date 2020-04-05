from django.test import TestCase

from django.contrib.auth.models import User


class ProfileModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(username='john', email='john@mail.com', password='John1234')

    def test_string_representation(self):
        ''' To ensure it is shown good in admin site. '''
        user = User.objects.get(username='john')
        self.assertEqual(str(user.profile), user.username)

    def test_profile_created_when_new_user_is_created(self):
        self.assertTrue(User.objects.get(username='john').profile)
