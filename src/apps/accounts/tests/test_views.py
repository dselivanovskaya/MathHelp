from django.conf import settings
from django.test import TestCase
from django.urls import reverse

from tests.data import USER_MALE, USER_FEMALE
from profiles.views import ProfileDetailView

from accounts.apps import AccountsConfig
from accounts.views import (
    AccountLoginView, AccountLogoutView,
    AccountCreateView, AccountDeleteView
)


class AccountLoginViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.url = reverse(AccountsConfig.ACCOUNT_LOGIN_URL)
        cls.view_class = AccountLoginView
        cls.user = USER_MALE.create_in_db()

    def test_anonymous_get_request(self):
        self.assertEqual(self.client.get(self.url).status_code, 200)

    def test_authenticated_get_request(self):
        self.client.login(username=USER_MALE.username, password=USER_MALE.password)
        self.assertEqual(self.client.get(self.url).status_code, 302)

    def test_successful_post_request(self):
        response = self.client.post(self.url, {
            'username': USER_MALE.username,
            'password': USER_MALE.password,
        }, follow=True)
        self.assertRedirects(response, self.user.profile.get_absolute_url())

    def test_unsuccessful_post_request(self):
        response = self.client.post(self.url, {
            'username': USER_FEMALE.username,
            'password': USER_FEMALE.password,
        })
        self.assertEqual(response.status_code, 200)

    def test_on_successful_login_increments_user_profile_login_count(self):
        login_count_before = self.user.profile.login_count
        self.client.post(self.url, {
            'username': USER_MALE.username,
            'password': USER_MALE.password,
        })
        self.user.refresh_from_db()
        self.assertEquals(login_count_before + 1, self.user.profile.login_count)

    def test_on_successful_login_initializes_session_entries(self):
        self.client.post(self.url, {
            'username': USER_MALE.username,
            'password': USER_MALE.password,
        })
        self.assertEquals(self.client.session['read_tickets'], [])
        self.assertEquals(self.client.session['taken_quizzes'], {})


class AccountLogoutViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.url = reverse(AccountsConfig.ACCOUNT_LOGOUT_URL)
        cls.view_class = AccountLogoutView
        cls.user = USER_MALE.create_in_db()

    def test_anonymous_get_request(self):
        self.assertEqual(self.client.get(self.url).status_code, 302)

    def test_authenticated_get_request(self):
        self.client.login(username=USER_MALE.username, password=USER_MALE.password)
        self.assertEqual(self.client.get(self.url).status_code, 302)

    def test_redirects_to_index_page(self):
        self.client.login(username=USER_MALE.username, password=USER_MALE.password)
        self.assertRedirects(
            self.client.get(self.url), reverse(settings.INDEX_URL)
        )


class AccountCreateViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.url = reverse(AccountsConfig.ACCOUNT_CREATE_URL)
        cls.view_class = AccountCreateView
        cls.user = USER_MALE.create_in_db()

    def test_anonymous_get_request(self):
        self.assertEqual(self.client.get(self.url).status_code, 200)

    def test_authenticated_get_request(self):
        self.client.login(username=USER_MALE.username, password=USER_MALE.password)
        self.assertEqual(self.client.get(self.url).status_code, 302)

    def test_redirects_authenticated_user_to_his_profile(self):
        self.client.login(username=USER_MALE.username, password=USER_MALE.password)
        response = self.client.get(self.url, follow=True)
        self.assertRedirects(response, self.user.profile.get_absolute_url())

    def test_on_successful_registration_redirects_user_to_login_page(self):
        response = self.client.post(self.url, {
            'first_name': USER_FEMALE.first_name,
            'last_name':  USER_FEMALE.last_name,
            'email':      USER_FEMALE.email,
            'username':   USER_FEMALE.username,
            'password1':  USER_FEMALE.password,
            'password2':  USER_FEMALE.password,
         })
        self.assertRedirects(response, reverse(settings.LOGIN_URL))

    def test_on_successful_registration_sends_correct_message(self):
        response = self.client.post(self.url, {
            'first_name': USER_FEMALE.first_name,
            'last_name':  USER_FEMALE.last_name,
            'email':      USER_FEMALE.email,
            'username':   USER_FEMALE.username,
            'password1':  USER_FEMALE.password,
            'password2':  USER_FEMALE.password,
         }, follow=True)
        messages = list(response.context['messages'])
        self.assertEquals(str(messages[0]), self.view_class.success_message)


class AccountDeleteViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.url = reverse(AccountsConfig.ACCOUNT_DELETE_URL)
        cls.view_class = AccountDeleteView
        USER_MALE.create_in_db()

    def test_anonymous_get_request(self):
        self.assertEqual(self.client.get(self.url).status_code, 302)

    def test_authenticated_get_request(self):
        self.client.login(username=USER_MALE.username, password=USER_MALE.password)
        self.assertEqual(self.client.get(self.url).status_code, 200)

    def test_after_delete_redirect_to_index_page(self):
        self.client.login(username=USER_MALE.username, password=USER_MALE.password)
        response = self.client.post(self.url, {})
        self.assertRedirects(response, reverse(settings.INDEX_URL))

    def test_on_delete_sends_corrent_message(self):
        self.client.login(username=USER_MALE.username, password=USER_MALE.password)
        response = self.client.post(self.url, {}, follow=True)
        messages = list(response.context['messages'])
        self.assertEquals(str(messages[0]), self.view_class.success_message)
