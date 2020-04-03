from django.test import TestCase

from django.contrib.auth.models import User

from .constants import MALE, FEMALE


class ProfilesTestCase(TestCase):

    def setUp(self):
        ''' Create two new users. '''
        self.username = 'harry'
        self.password = 'hogwarts200'
        self.email    = 'potter@mail.com'
        self.user     = User.objects.create_user(username=self.username,
                                                 email=self.email,
                                                 password=self.password)
        self.username2 = 'ron'
        self.password2 = 'sweets32'
        self.email2    = 'weasley@mail.com'
        self.user2     = User.objects.create_user(username=self.username2,
                                                  email=self.email,
                                                  password=self.password)

    def test_profile_is_automatically_created_when_new_user_is_created(self):
        self.assertTrue(self.user.profile)

    def test_user_gender_can_be_set_through_user_model(self):
        self.user.profile.gender = MALE
        self.assertEquals(self.user.profile.gender, MALE)

    def test_unauthenticated_user_can_not_access_any_user_profile(self):
        response = self.client.get(f'/{self.username}')
        self.assertRedirects(response, '/')

    def test_unauthenticated_user_can_not_delete_any_other_user_profile(self):
        before_delete_user_count = User.objects.count()
        response = self.client.get(f'/{self.username}/delete')
        self.assertEquals(before_delete_user_count, User.objects.count())

    def test_authenticated_user_can_not_access_any_other_user_profile(self):
        self.client.login(username = self.username, password=self.password)
        response = self.client.get(f'/{self.username2}')
        self.assertRedirects(response, '/')

    def test_authenticated_user_can_not_delete_any_other_user_profile(self):
        before_delete_user_count = User.objects.count()
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(f'/{self.username2}/delete')
        self.assertEquals(before_delete_user_count, User.objects.count())

    def test_user_can_delete_his_profile(self):
        before_delete_user_count = User.objects.count()
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(f'/{self.username}/delete')
        self.assertEquals(before_delete_user_count - 1, User.objects.count())

