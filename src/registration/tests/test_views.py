from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from registration.forms import RegistrationForm


class RegisterUserViewTest(TestCase):
    ''' Tests for 'register_user' view. '''

    @classmethod
    def setUpTestData(cls):
        cls.url  = '/register/'
        cls.name = 'register'
        cls.template = 'registration/register.html'
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
        self.assertIsInstance(response.context['form'], RegistrationForm)

    def test_redirects_authenticated_user_to_home(self):
        self.client.login(username='john', password='johny123')
        self.assertRedirects(self.client.get(self.url), '/')

    def test_on_successful_registration_redirects_user_to_his_profile(self):
        response = self.client.post(self.url, {
            'username' : 'alice',
            'email'    : 'alice@mail.com',
            'password1': 'alice1234',
            'password2': 'alice1234',
         }, follow=True)
        self.assertRedirects(response, '/alice')

    def test_on_unsuccessful_registration_doesnt_redirect_user_to_his_profile(self):
        response = self.client.post(self.url, {
            'username' : 'alice',
            'email'    : 'alice@mail.com',
            'password1': 'alice1234',
            'password2': 'ALICE1234',
         })
        self.assertEqual(response.status_code, 200)

    def test_on_successful_registration_renders_correct_template(self):
        response = self.client.post(self.url, {
            'username' : 'alice',
            'email'    : 'alice@mail.com',
            'password1': 'alice1234',
            'password2': 'alice1234',
        }, follow=True)
        self.assertTemplateUsed(response, 'profiles/user-profile.html')

    def test_on_unsuccessful_registration_renders_correct_template(self):
        response = self.client.post(self.url, {
            'username' : 'alice',
            'email'    : 'alice@mail.com',
            'password1': 'alice1234',
            'password2': 'ALICE1234',
        })
        self.assertTemplateUsed(response, self.template)
