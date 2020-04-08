from django.contrib.auth.models import User
from django.test import TestCase, TransactionTestCase
from django.urls import reverse

from authentication.forms import LoginForm


class LoginUserViewTest(TestCase):
    ''' Tests for 'login_user' view. '''

    @classmethod
    def setUpTestData(cls):
        cls.url  = '/login/'
        cls.name = 'login'
        cls.template = 'authentication/login.html'
        User.objects.create_user(
            username='john', email='john@mail.com', password='johny123'
        )

    def test_view_url_exists(self):
        self.assertEqual(self.client.get(self.url).status_code, 200)

    def test_view_url_accessible_by_name(self):
        self.assertEqual(self.client.get(reverse(self.name)).status_code, 200)

    def test_view_renders_correct_template(self):
        self.assertTemplateUsed(self.client.get(reverse(self.name)), self.template)

    def test_view_renders_correct_form(self):
        response = self.client.get(self.url)
        self.assertIsInstance(response.context['form'], LoginForm)

    def test_redirects_authenticated_user_to_home(self):
        self.client.login(username='john', password='johny123')
        self.assertRedirects(self.client.get(self.url), '/')

    def test_existing_user_can_successfully_log_in(self):
        self.assertTrue(self.client.login(username='john', password='johny123'))

    def test_on_successful_login_redirects_user_to_his_profile(self):
        response = self.client.post(self.url,
            {'username': 'john', 'password': 'johny123'},
        )
        self.assertRedirects(response, '/profile/')

    def test_on_unsuccessful_login_doesnt_redirect_user_to_his_profile(self):
        response = self.client.post(self.url,
            {'username': 'alice', 'password': 'alice123'},
        )
        self.assertEqual(response.status_code, 200)

    def test_on_successful_login_renders_correct_template(self):
        response = self.client.post(self.url,
            {'username': 'john', 'password': 'johny123'}, follow=True
        )
        self.assertTemplateUsed(response, 'profile/get-profile.html')

    def test_on_unsuccessful_login_renders_correct_template(self):
        response = self.client.post(self.url,
            {'username': 'alice', 'password': 'alice123'}
        )
        self.assertTemplateUsed(response, self.template)

    def test_on_successful_login_increments_user_profile_login_count(self):
        user = User.objects.get(username='john')
        login_count_before = user.profile.login_count
        self.client.post(self.url, {'username': 'john', 'password': 'johny123'})
        user.refresh_from_db()
        self.assertEquals(login_count_before + 1, user.profile.login_count)


class LogoutUserViewTest(TestCase):
    ''' Tests for 'logout_user' view. '''

    @classmethod
    def setUpTestData(cls):
        cls.url  = '/logout/'
        cls.name = 'logout'

    def test_view_url_exists(self):
        response = self.client.get(self.url, follow=True)
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse(self.name), follow=True)
        self.assertEqual(response.status_code, 200)

    def test_redirects_to_home_page(self):
        response = self.client.get(self.url, follow=True)
        self.assertRedirects(response, '/')
