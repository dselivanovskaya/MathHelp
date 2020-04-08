from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from registration.forms import RegistrationForm


class RegisterUserViewTest(TestCase):
    ''' Tests for 'register_user' view. '''

    JOHN_USERNAME = 'john'
    JOHN_EMAIL = 'john@mail.com'
    JOHN_PASSWORD = 'John_123'

    ALICE_USERNAME = 'alice'
    ALICE_EMAIL = 'alice@gmail.com'
    ALICE_PASSOWRD = 'Alice_123'

    @classmethod
    def setUpTestData(cls):
        cls.url  = '/register/'
        cls.name = 'register'
        cls.template = 'registration/registration.html'
        User.objects.create_user(
            username=cls.JOHN_USERNAME,
            email=cls.JOHN_EMAIL,
            password=cls.JOHN_PASSWORD
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
        self.client.login(
            username=self.JOHN_USERNAME, password=self.JOHN_PASSWORD
        )
        self.assertRedirects(self.client.get(self.url), '/')

    def test_on_successful_registration_redirects_user_to_his_profile(self):
        response = self.client.post(self.url, {
            'username' : self.ALICE_USERNAME,
            'email'    : self.ALICE_EMAIL,
            'password1': self.ALICE_PASSOWRD,
            'password2': self.ALICE_PASSOWRD,
         })
        self.assertRedirects(response, '/profile/')

    def test_on_unsuccessful_registration_doesnt_redirect_user_to_his_profile(self):
        response = self.client.post(self.url, {
            'username' : self.ALICE_USERNAME,
            'email'    : self.ALICE_EMAIL,
            'password1': self.ALICE_PASSOWRD,
            'password2': self.ALICE_PASSOWRD + ')',
         })
        self.assertEqual(response.status_code, 200)

    def test_on_successful_registration_renders_correct_template(self):
        response = self.client.post(self.url, {
            'username' : self.ALICE_USERNAME,
            'email'    : self.ALICE_EMAIL,
            'password1': self.ALICE_PASSOWRD,
            'password2': self.ALICE_PASSOWRD,
        }, follow=True)
        self.assertTemplateUsed(response, 'profile/get-profile.html')

    def test_on_unsuccessful_registration_renders_correct_template(self):
        response = self.client.post(self.url, {
            'username' : self.ALICE_USERNAME,
            'email'    : self.ALICE_EMAIL,
            'password1': self.ALICE_PASSOWRD,
            'password2': self.ALICE_PASSOWRD + ')',
        })
        self.assertTemplateUsed(response, self.template)
