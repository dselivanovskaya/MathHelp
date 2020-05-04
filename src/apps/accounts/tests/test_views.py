from django.conf import settings
from django.test import TestCase
from django.urls import reverse

from tests.data import MALE_USER, FEMALE_USER
from profiles.views import ProfileDetailView

from accounts.apps import AccountsConfig
from accounts.views import (
    AccountLoginView, AccountLogoutView, AccountCreateView, AccountDeleteView
)


class AccountLoginViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = MALE_USER.create()
        cls.url = reverse(AccountsConfig.ACCOUNT_LOGIN_URL)
        cls.view_class = AccountLoginView

    def test_anonymous_get_request(self):
        self.assertEqual(self.client.get(self.url).status_code, 200)

    def test_authenticated_get_request(self):
        self.client.login(username=MALE_USER.username, password=MALE_USER.password)
        self.assertEqual(self.client.get(self.url).status_code, 302)

    def test_successful_post_request(self):
        response = self.client.post(self.url, {
            'username': MALE_USER.username,
            'password': MALE_USER.password,
        }, follow=True)
        self.assertRedirects(response, self.user.profile.get_absolute_url())

    def test_unsuccessful_post_request(self):
        response = self.client.post(self.url, {
            'username': FEMALE_USER.username,
            'password': FEMALE_USER.password,
        })
        self.assertEqual(response.status_code, 200)

    def test_on_successful_login_increments_user_profile_login_count(self):
        login_count_before = self.user.profile.login_count
        self.client.post(self.url, {
            'username': MALE_USER.username,
            'password': MALE_USER.password,
        })
        self.user.refresh_from_db()
        self.assertEquals(login_count_before + 1, self.user.profile.login_count)

    def test_on_successful_login_initializes_session_entries(self):
        self.client.post(self.url, {
            'username': MALE_USER.username,
            'password': MALE_USER.password,
        })
        self.assertEquals(self.client.session['read_tickets'], [])
        self.assertEquals(self.client.session['taken_quizzes'], {})


class AccountLogoutViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = MALE_USER.create()
        cls.url = reverse(AccountsConfig.ACCOUNT_LOGOUT_URL)
        cls.view_class = AccountLogoutView

    def test_anonymous_get_request(self):
        self.assertEqual(self.client.get(self.url).status_code, 302)

    def test_authenticated_get_request(self):
        self.client.login(username=MALE_USER.username, password=MALE_USER.password)
        self.assertEqual(self.client.get(self.url).status_code, 302)

    def test_redirects_to_index_page(self):
        self.client.login(username=MALE_USER.username, password=MALE_USER.password)
        self.assertRedirects(
            self.client.get(self.url), reverse(settings.INDEX_URL)
        )


class AccountCreateViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = MALE_USER.create()
        cls.url = reverse(AccountsConfig.ACCOUNT_CREATE_URL)
        cls.view_class = AccountCreateView

    def test_anonymous_get_request(self):
        self.assertEqual(self.client.get(self.url).status_code, 200)

    def test_authenticated_get_request(self):
        self.client.login(username=MALE_USER.username, password=MALE_USER.password)
        self.assertEqual(self.client.get(self.url).status_code, 302)

    def test_redirects_authenticated_user_to_his_profile(self):
        self.client.login(username=MALE_USER.username, password=MALE_USER.password)
        response = self.client.get(self.url, follow=True)
        self.assertRedirects(response, self.user.profile.get_absolute_url())

    def test_on_successful_registration_redirects_user_to_login_page(self):
        response = self.client.post(self.url, {
            'first_name': FEMALE_USER.first_name,
            'last_name':  FEMALE_USER.last_name,
            'email':      FEMALE_USER.email,
            'username':   FEMALE_USER.username,
            'password1':  FEMALE_USER.password,
            'password2':  FEMALE_USER.password,
         })
        self.assertRedirects(response, reverse(settings.LOGIN_URL))

    def test_on_successful_registration_sends_correct_message(self):
        response = self.client.post(self.url, {
            'first_name': FEMALE_USER.first_name,
            'last_name':  FEMALE_USER.last_name,
            'email':      FEMALE_USER.email,
            'username':   FEMALE_USER.username,
            'password1':  FEMALE_USER.password,
            'password2':  FEMALE_USER.password,
         }, follow=True)
        messages = list(response.context['messages'])
        self.assertEquals(str(messages[0]), self.view_class.success_message)


class AccountDeleteViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        MALE_USER.create()
        cls.url = reverse(AccountsConfig.ACCOUNT_DELETE_URL)
        cls.view_class = AccountDeleteView

    def test_anonymous_get_request(self):
        self.assertEqual(self.client.get(self.url).status_code, 302)

    def test_authenticated_get_request(self):
        self.client.login(username=MALE_USER.username, password=MALE_USER.password)
        self.assertEqual(self.client.get(self.url).status_code, 200)

    def test_after_delete_redirect_to_index_page(self):
        self.client.login(username=MALE_USER.username, password=MALE_USER.password)
        response = self.client.post(self.url, {})
        self.assertRedirects(response, reverse(settings.INDEX_URL))

    def test_on_delete_sends_corrent_message(self):
        self.client.login(username=MALE_USER.username, password=MALE_USER.password)
        response = self.client.post(self.url, {}, follow=True)
        messages = list(response.context['messages'])
        self.assertEquals(str(messages[0]), self.view_class.success_message)
