from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from registration.forms import SignUpForm

JOHN_USERNAME, ALICE_USERNAME = 'john', 'alice'
JOHN_EMAIL, ALICE_EMAIL = 'john@mail.com', 'alice@mail.com'
JOHN_PASSWORD, ALICE_PASSWORD = 'johny_123', 'alicia_123'

class SignUpViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.url = '/sign-up'
        cls.name = 'sign-up'
        cls.template = 'registration/registration.html'
        User.objects.create_user(
            username=JOHN_USERNAME, email=JOHN_EMAIL, password=JOHN_PASSWORD
        )

    def test_view_url_exists(self):
        self.assertEqual(self.client.get(self.url).status_code, 200)

    def test_view_url_accessible_by_name(self):
        self.assertEqual(self.client.get(reverse(self.name)).status_code, 200)

    def test_view_renders_correct_template(self):
        self.assertTemplateUsed(self.client.get(reverse(self.name)), self.template)

    def test_view_renders_correct_form(self):
        response = self.client.get(self.url)
        self.assertIsInstance(response.context['form'], SignUpForm)

    def test_redirects_authenticated_user_to_home(self):
        self.client.login(username=JOHN_USERNAME, password=JOHN_PASSWORD)
        self.assertRedirects(self.client.get(self.url), '/')

    def test_on_successful_registration_redirects_user_to_his_profile(self):
        response = self.client.post(self.url, {
            'username': ALICE_USERNAME, 'email': ALICE_EMAIL,
            'password1': ALICE_PASSWORD, 'password2': ALICE_PASSWORD,
         })
        self.assertRedirects(response, '/profile')

    def test_on_unsuccessful_registration_doesnt_redirect_user_to_his_profile(self):
        response = self.client.post(self.url, {
            'username': ALICE_USERNAME, 'email': ALICE_EMAIL,
            'password1': ALICE_PASSWORD, 'password2': ALICE_PASSWORD + ')',
         })
        self.assertEqual(response.status_code, 200)

    def test_on_successful_registration_renders_correct_template(self):
        response = self.client.post(self.url, {
            'username': ALICE_USERNAME, 'email': ALICE_EMAIL,
            'password1': ALICE_PASSWORD, 'password2': ALICE_PASSWORD,
        }, follow=True)
        self.assertTemplateUsed(response, 'profile/profile.html')

    def test_on_unsuccessful_registration_renders_correct_template(self):
        response = self.client.post(self.url, {
            'username': ALICE_USERNAME, 'email': ALICE_EMAIL,
            'password1': ALICE_PASSWORD, 'password2': ALICE_PASSWORD + ')',
        })
        self.assertTemplateUsed(response, self.template)
