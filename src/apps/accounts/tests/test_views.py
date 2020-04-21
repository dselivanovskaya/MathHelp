from django.conf import settings
from django.test import TestCase
from django.urls import reverse

from tests.data import USER1, USER2
from profiles.views import ProfileDetailView

from accounts.apps import AccountsConfig as accounts_config
from accounts.views import (
    AccountLoginView, AccountLogoutView,
    AccountSettingsView,
    AccountCreateView, AccountDeleteView
)


class AccountLoginViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.url = reverse(accounts_config.ACCOUNT_LOGIN_URL)
        cls.view_class = AccountLoginView
        cls.form_class = cls.view_class.form_class
        cls.template_name = cls.view_class.template_name
        cls.user = USER1.create_in_db()

    def test_url_exists(self):
        self.assertEqual(self.client.get(self.url).status_code, 200)

    def test_renders_correct_form(self):
        response = self.client.get(self.url)
        self.assertIsInstance(response.context['form'], self.form_class)

    def test_renders_correct_template(self):
        self.assertTemplateUsed(self.client.get(self.url), self.template_name)

    def test_redirects_authenticated_user_to_his_profile(self):
        self.client.login(username=USER1.username, password=USER1.password)
        response = self.client.get(self.url, follow=True)
        self.assertEquals(response.redirect_chain, [
            (reverse(settings.LOGIN_REDIRECT_URL), 302),
            (f'/profiles/{USER1.username}', 302)
         ])

    def test_on_successful_login_redirects_user_to_his_profile(self):
        response = self.client.post(self.url, {
            'username': USER1.username,
            'password': USER1.password,
        }, follow=True)
        self.assertRedirects(response, f'/profiles/{USER1.username}')

    def test_on_unsuccessful_login_doesnt_redirect_user_to_his_profile(self):
        response = self.client.post(self.url, {
            'username': USER2.username,
            'password': USER2.password,
        })
        self.assertEqual(response.status_code, 200)

    def test_on_successful_login_renders_correct_template(self):
        response = self.client.post(self.url, {
            'username': USER1.username,
            'password': USER1.password,
        }, follow=True)
        self.assertTemplateUsed(response, ProfileDetailView.template_name)

    def test_on_unsuccessful_login_renders_correct_template(self):
        response = self.client.post(self.url, {
            'username': USER2.username,
            'password': USER2.password,
        }, follow=True)
        self.assertTemplateUsed(response, self.template_name)

    def test_on_successful_login_increments_user_profile_login_count(self):
        login_count_before = self.user.profile.login_count
        self.client.post(self.url, {
            'username': USER1.username,
            'password': USER1.password,
        })
        self.user.refresh_from_db()
        self.assertEquals(login_count_before + 1, self.user.profile.login_count)

    def test_on_successful_login_initializes_session_entries(self):
        self.client.post(self.url, {
            'username': USER1.username,
            'password': USER1.password,
        })
        self.assertEquals(self.client.session['watched_tickets'], [])


class AccountLogoutViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.url = reverse(accounts_config.ACCOUNT_LOGOUT_URL)
        cls.view_class = AccountLogoutView
        cls.user = USER1.create_in_db()

    def test_view_url_exists(self):
        self.client.login(username=USER1.username, password=USER1.password)
        self.assertEqual(
            self.client.get(self.url, follow=True).status_code, 200
        )

    def test_redirects_anonymous_user_to_login_page(self):
        self.assertRedirects(
            self.client.get(self.url), reverse(settings.LOGIN_URL)
        )

    def test_redirects_to_index_page(self):
        self.client.login(username=USER1.username, password=USER1.password)
        self.assertRedirects(
            self.client.get(self.url), reverse(settings.INDEX_URL)
        )

    def test_sends_correct_message(self):
        self.client.login(username=USER1.username, password=USER1.password)
        response = self.client.get(self.url, follow=True)
        messages = list(response.context['messages'])
        self.assertEquals(str(messages[0]), self.view_class.messages['success'])


def AccountSettingsViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.url = reverse(accounts_config.ACCOUNT_SETTINGS_URL)
        cls.view_class = AccountSettingsView
        cls.template_name = cls.view_class.template_name
        USER1.create_in_db()

    def test_url_exists_for_authenticated_user(self):
        self.client.login(username=USER1.username, password=USER1.password)
        self.assertEqual(self.client.get(self.url).status_code, 200)

    def test_renders_correct_template_for_authenticated_user(self):
        self.client.login(username=USER1.username, password=USER1.password)
        self.assertTemplateUsed(self.client.get(self.url), self.template_name)

    def test_redirects_anonymous_user_to_login_page(self):
        self.assertRedirects(
            self.client.get(self.url), reverse(settings.LOGIN_URL)
        )


class AccountCreateViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.url = reverse(accounts_config.ACCOUNT_CREATE_URL)
        cls.view_class = AccountCreateView
        cls.form_class = cls.view_class.form_class
        cls.template_name = cls.view_class.template_name
        cls.user = USER1.create_in_db()

    def test_url_exists(self):
        self.assertEqual(self.client.get(self.url).status_code, 200)

    def test_renders_correct_form(self):
        response = self.client.get(self.url)
        self.assertIsInstance(response.context['form'], self.form_class)

    def test_renders_correct_template(self):
        self.assertTemplateUsed(self.client.get(self.url), self.template_name)

    def test_redirects_authenticated_user_to_his_profile(self):
        self.client.login(username=USER1.username, password=USER1.password)
        response = self.client.get(self.url, follow=True)
        self.assertEquals(response.redirect_chain, [
            (reverse(settings.LOGIN_REDIRECT_URL), 302),
            (f'/profiles/{USER1.username}', 302)
         ])

    def test_on_successful_registration_redirects_user_to_login_page(self):
        response = self.client.post(self.url, {
            'first_name': USER2.first_name,
            'last_name':  USER2.last_name,
            'email':      USER2.email,
            'username':   USER2.username,
            'password1':  USER2.password,
            'password2':  USER2.password,
         })
        self.assertRedirects(response, reverse(settings.LOGIN_URL))

    def test_on_successful_registration_sends_correct_message(self):
        response = self.client.post(self.url, {
            'first_name': USER2.first_name,
            'last_name':  USER2.last_name,
            'email':      USER2.email,
            'username':   USER2.username,
            'password1':  USER2.password,
            'password2':  USER2.password,
         }, follow=True)
        messages = list(response.context['messages'])
        self.assertEquals(str(messages[0]), self.view_class.messages['success'])

    def test_on_unsuccessful_registration_doesnt_redirect_user(self):
        response = self.client.post(self.url, {
            'first_name': USER2.first_name,
            'last_name':  USER2.last_name,
            'email':      USER2.email,
            'username':   USER2.username,
            'password1':  USER2.password,
            'password2':  USER2.password + '>',
         })
        self.assertEqual(response.status_code, 200)

    def test_on_successful_registration_renders_correct_template(self):
        response = self.client.post(self.url, {
            'first_name': USER2.first_name,
            'last_name':  USER2.last_name,
            'email':      USER2.email,
            'username':   USER2.username,
            'password1':  USER2.password,
            'password2':  USER2.password,
        }, follow=True)
        self.assertTemplateUsed(response, AccountLoginView.template_name)

    def test_on_unsuccessful_registration_renders_correct_template(self):
        response = self.client.post(self.url, {
            'first_name': USER2.first_name,
            'last_name':  USER2.last_name,
            'email':      USER2.email,
            'username':   USER2.username,
            'password1':  USER2.password,
            'password2':  USER2.password + '>',
         }, follow=True)
        self.assertTemplateUsed(response, self.template_name)


class AccountDeleteViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.url = reverse(accounts_config.ACCOUNT_DELETE_URL)
        cls.view_class = AccountDeleteView
        cls.template_name = cls.view_class.template_name
        USER1.create_in_db()

    def test_url_exists_for_authenticated_user(self):
        self.client.login(username=USER1.username, password=USER1.password)
        self.assertEqual(self.client.get(self.url).status_code, 200)

    def test_renders_correct_template_for_authenticated_user(self):
        self.client.login(username=USER1.username, password=USER1.password)
        self.assertTemplateUsed(self.client.get(self.url), self.template_name)

    def test_redirects_anonymous_user_to_login_page(self):
        self.assertRedirects(
            self.client.get(self.url), reverse(settings.LOGIN_URL)
        )

    def test_after_delete_redirect_to_index_page(self):
        self.client.login(username=USER1.username, password=USER1.password)
        response = self.client.post(self.url, {})
        self.assertRedirects(response, reverse(settings.INDEX_URL))

    def test_on_delete_sends_corrent_message(self):
        self.client.login(username=USER1.username, password=USER1.password)
        response = self.client.post(self.url, {}, follow=True)
        messages = list(response.context['messages'])
        self.assertEquals(str(messages[0]), self.view_class.messages['success'])
