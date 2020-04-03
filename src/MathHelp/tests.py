from django.test import TestCase
from django.contrib.auth.models import User

from profiles.models import Profile
from profiles.constants import MALE, FEMALE

from .constants import FAIL_LOGIN_ERROR_MESSAGE


class LoginTestCase(TestCase):

    def setUp(self):
        ''' Create a new user. '''

        self.login_url = '/login/'
        self.username  = 'john'
        self.email     = 'john@mail.com'
        self.password  = 'knowledge4U'
        self.user      = User.objects.create_user(username=self.username,
                                                 email=self.email,
                                                 password=self.password)
        self.user.profile.gender = MALE
        self.user.save()

    def test_login_url_exists(self):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)

    def test_existing_user_can_log_in(self):
        login = self.client.login(username=self.username, password=self.password)
        self.assertTrue(login)

    def test_successful_login_redirects_user_to_his_profile(self):
        response = self.client.post(self.login_url,
                   {
                       'username': self.username,
                       'password': self.password,
                   })
        self.assertRedirects(response, f'/{self.username}')

    def test_successful_login_returns_user_profile_page(self):
        response = self.client.post(self.login_url,
                   {
                       'username': self.username,
                       'password': self.password,
                   }, follow=True)
        self.assertTemplateUsed(response, 'profiles/user-profile.html')

    def test_fail_login_returns_login_page_again(self):
        response = self.client.post(self.login_url,
                   {
                       'username': 'unknown',
                       'password': 'unknown',
                   })
        self.assertTemplateUsed(response, 'login.html')

    def test_fail_login_returns_error_message(self):
        response = self.client.post(self.login_url,
                   {
                       'username': 'unknown',
                       'password': 'unknown',
                   })
        self.assertContains(response, FAIL_LOGIN_ERROR_MESSAGE)

    def test_logged_in_user_is_redirected_to_his_profile_if_tries_login_again(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(self.login_url)
        self.assertRedirects(response, f'/{self.username}')

    # Doesn't work
    def test_successful_login_increments_user_profile_login_count(self):
        login_count_before = self.user.profile.login_count
        response = self.client.post(self.login_url,
                   {
                       'username': self.username,
                       'password': self.password,
                   })
        print(response)
        print(repr(self.user))
        print(repr(self.user.profile))
        self.assertEquals(login_count_before + 1, self.user.profile.login_count)


class LogoutTestCase(TestCase):

    def setUp(self):
        self.logout_url = '/logout/'

    def test_logout_url_redirects_to_home_page(self):
        response = self.client.get(self.logout_url)
        self.assertRedirects(response, '/')
