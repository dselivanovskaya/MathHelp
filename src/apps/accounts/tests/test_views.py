from django.conf import settings
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from accounts.views import SigninView, SignupView

from .test_data import USER1, USER2


class SigninViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.url = reverse(settings.LOGIN_URL)
        cls.form_class = SigninView.form_class
        cls.template_name = SigninView.template_name
        User.objects.create_user(
            username=USER1.username, email=USER1.email, password=USER1.password
        )

    def test_view_url_exists(self):
        self.assertEqual(self.client.get(self.url).status_code, 200)

    def test_view_renders_correct_form(self):
        response = self.client.get(self.url)
        self.assertIsInstance(response.context['form'], self.form_class)

    def test_view_renders_correct_template(self):
        self.assertTemplateUsed(self.client.get(self.url), self.template_name)

    def test_redirects_authenticated_user(self):
        self.client.login(username=USER1.username, password=USER1.password)
        response = self.client.get(self.url, follow=True)
        self.assertEquals(response.redirect_chain, [
            (reverse(settings.LOGIN_REDIRECT_URL), 302),
            (f'/{USER1.username}', 302)
         ])

    def test_on_successful_login_redirects_user(self):
        response = self.client.post(self.url, {
            'username': USER1.username,
            'password': USER1.password,
        }, follow=True)
        self.assertEquals(response.redirect_chain, [
            (reverse(settings.LOGIN_REDIRECT_URL), 302),
            (f'/{USER1.username}', 302)
         ])

    def test_on_unsuccessful_login_doesnt_redirect_user(self):
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
        self.assertTemplateUsed(response, 'profiles/profile.html')

    def test_on_unsuccessful_login_renders_correct_template(self):
        response = self.client.post(self.url, {
            'username': USER2.username,
            'password': USER2.password,
        }, follow=True)
        self.assertTemplateUsed(response, self.template_name)

    def test_on_successful_login_increments_user_profile_login_count(self):
        user = User.objects.get(username=USER1.username)
        login_count_before = user.profile.login_count
        self.client.post(self.url, {
            'username': USER1.username,
            'password': USER1.password,
        })
        user.refresh_from_db()
        self.assertEquals(login_count_before + 1, user.profile.login_count)

    def test_on_successful_login_initializes_session_entries(self):
        self.client.post(self.url, {
            'username': USER1.username,
            'password': USER1.password,
        })
        self.assertEquals(self.client.session['watched_tickets'], [])


class SignupViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.url = reverse(settings.REGISTER_URL)
        cls.form_class = SignupView.form_class
        cls.template_name = SignupView.template_name
        User.objects.create_user(
            username=USER1.username, email=USER1.email, password=USER1.password
        )

    def test_view_url_exists(self):
        self.assertEqual(self.client.get(self.url).status_code, 200)

    def test_view_renders_correct_template(self):
        self.assertTemplateUsed(self.client.get(self.url), self.template_name)

    def test_view_renders_correct_form(self):
        response = self.client.get(self.url)
        self.assertIsInstance(response.context['form'], self.form_class)

    def test_redirects_authenticated_user(self):
        self.client.login(username=USER1.username, password=USER1.password)
        response = self.client.get(self.url, follow=True)
        self.assertEquals(response.redirect_chain, [
            (reverse(settings.LOGIN_REDIRECT_URL), 302),
            (f'/{USER1.username}', 302)
         ])

    def test_on_successful_registration_redirects_user(self):
        response = self.client.post(self.url, {
            'full_name': USER2.full_name,
            'email':     USER2.email,
            'username':  USER2.username,
            'password1': USER2.password,
            'password2': USER2.password,
         })
        self.assertRedirects(response, reverse(settings.LOGIN_URL))

    def test_on_unsuccessful_registration_doesnt_redirect(self):
        response = self.client.post(self.url, {
            'full_name': USER2.full_name,
            'email':     USER2.email,
            'username':  USER2.username,
            'password1': USER2.password,
            'password2': USER2.password + 'l',
         })
        self.assertEqual(response.status_code, 200)

    def test_on_successful_registration_renders_correct_template(self):
        response = self.client.post(self.url, {
            'full_name': USER2.full_name,
            'email':     USER2.email,
            'username':  USER2.username,
            'password1': USER2.password,
            'password2': USER2.password,
        }, follow=True)
        self.assertTemplateUsed(response, SigninView.template_name)

    def test_on_unsuccessful_registration_renders_correct_template(self):
        response = self.client.post(self.url, {
            'full_name': USER2.full_name,
            'email':     USER2.email,
            'username':  USER2.username,
            'password1': USER2.password,
            'password2': USER2.password + 'l',
         })
        self.assertTemplateUsed(response, self.template_name)


class SignoutViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.url = reverse(settings.LOGOUT_URL)

    def test_view_url_exists(self):
        self.assertEqual(
            self.client.get(self.url, follow=True).status_code, 200
        )

    def test_redirects(self):
        self.assertRedirects(
            self.client.get(self.url), reverse(settings.LOGOUT_REDIRECT_URL)
        )
