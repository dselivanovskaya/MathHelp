from django.contrib.auth.models import User
from django.test import TestCase

from registration.forms import SignUpForm


JOHN_USERNAME = 'john'
JOHN_EMAIL = 'john@mail.com'
JOHN_PASSWORD = 'johny_123'

ALICE_USERNAME = 'alice'
ALICE_EMAIL = 'alice@gmail.com'
ALICE_PASSWORD = 'alicia_123'


class SignUpFormTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.view_url = '/sign-up'
        User.objects.create_user(
            username=JOHN_USERNAME, email=JOHN_EMAIL, password=JOHN_PASSWORD
        )

    def test_form_is_invalid_if_username_is_not_available(self):
        form = SignUpForm({
            'username' : JOHN_USERNAME,
            'email'    : ALICE_EMAIL,
            'password1': ALICE_PASSWORD,
            'password2': ALICE_PASSWORD,
        })
        self.assertFalse(form.is_valid())

    def test_form_is_invalid_if_email_is_not_available(self):
        form = SignUpForm({
            'username' : ALICE_USERNAME,
            'email'    : JOHN_EMAIL,
            'password1': ALICE_PASSWORD,
            'password2': ALICE_PASSWORD,
        })
        self.assertFalse(form.is_valid())

    def test_form_is_invalid_if_passwords_dont_match(self):
        form = SignUpForm({
            'username' : ALICE_USERNAME,
            'email'    : ALICE_EMAIL,
            'password1': ALICE_PASSWORD,
            'password2': ALICE_PASSWORD + '0',
        })
        self.assertFalse(form.is_valid())

    def test_form_is_invalid_if_password_doesnt_have_one_digit(self):
        form = SignUpForm({
            'username' : ALICE_USERNAME,
            'email'    : ALICE_EMAIL,
            'password1': 'aliceiscool',
            'password1': 'aliceiscool',
        })
        self.assertFalse(form.is_valid())

    def test_form_is_invalid_if_password_doesnt_have_one_special_character(self):
        form = SignUpForm({
            'username' : ALICE_USERNAME,
            'email'    : ALICE_EMAIL,
            'password1': 'aliceIsCool12',
            'password2': 'aliceIsCool12',
        })
        self.assertFalse(form.is_valid())

    def test_form_displays_correct_error_message_if_username_is_not_available(self):
        response = self.client.post(self.view_url, {
            'username' : JOHN_USERNAME,
            'email'    : ALICE_EMAIL,
            'password1': ALICE_PASSWORD,
            'password2': ALICE_PASSWORD,
        })
        self.assertFormError(response,
            'form', 'username', 'User with that username already exists.'
        )

    def test_form_displays_correct_error_message_if_email_is_not_available(self):
        response = self.client.post(self.view_url, {
            'username' : ALICE_USERNAME,
            'email'    : JOHN_EMAIL,
            'password1': ALICE_PASSWORD,
            'password2': ALICE_PASSWORD,
         })
        self.assertFormError(response,
            'form', 'email', 'User with that email already exists.'
        )

    def test_form_displays_correct_error_message_if_password_doesnt_have_one_digit(self):
        response = self.client.post(self.view_url, {
            'username' : ALICE_USERNAME,
            'email'    : ALICE_EMAIL,
            'password1': 'aliceiscool',
            'password2': 'aliceiscool',
        })
        self.assertFormError(response,
            'form', 'password2', 'Password must contain at least 1 digit.'
        )

    def test_form_displays_correct_error_message_if_password_doesnt_have_one_special_character(self):
        response = self.client.post(self.view_url, {
            'username' : ALICE_USERNAME,
            'email'    : ALICE_EMAIL,
            'password1': 'aliceIsCool12',
            'password2': 'aliceIsCool12',
        })
        self.assertFormError(response,
            'form', 'password2', 'Password must contain at least 1 of these '
            'characters [~\!@#\$%\^&\*\(\)_\+{}":;\'\[\]].'
        )
