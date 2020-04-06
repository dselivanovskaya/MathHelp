from django.contrib.auth.models import User
from django.test import TestCase

from registration.forms import RegistrationForm


class RegistrationFormTest(TestCase):
    ''' Tests for RegistrationForm. '''

    @classmethod
    def setUpTestData(cls):
        cls.view_url = '/register/'
        User.objects.create_user(
            username='john', email='john@mail.com', password='johny123'
        )

    def test_username_field_placeholder(self):
        form = RegistrationForm()
        self.assertEqual(
            form.fields['username'].widget.attrs['placeholder'], 'example'
        )

    def test_email_field_placeholder(self):
        form = RegistrationForm()
        self.assertEqual(
            form.fields['email'].widget.attrs['placeholder'], 'example@gmail.com'
        )

    def test_password_field_help_text(self):
        form = RegistrationForm()
        self.assertEqual(form.fields['password1'].help_text, '8 characters min.')

    def test_repeat_password_field_help_text(self):
        form = RegistrationForm()
        self.assertEqual(form.fields['password2'].help_text, '8 characters min.')

    def test_form_is_invalid_if_username_is_not_available(self):
        form = RegistrationForm({
            'username' : 'john',
            'email'    : 'alice@mail.com',
            'password1': 'alice1234',
            'password2': 'alice1234',
        })
        self.assertFalse(form.is_valid())

    def test_form_is_invalid_if_email_is_not_available(self):
        form = RegistrationForm({
            'username' : 'alice',
            'email'    : 'john@mail.com',
            'password1': 'alice1234',
            'password2': 'alice1234',
        })
        self.assertFalse(form.is_valid())

    def test_form_is_invalid_if_passwords_dont_match(self):
        form = RegistrationForm({
            'username' : 'alice',
            'email'    : 'alice@mail.com',
            'password1': 'alice1234',
            'password2': 'ALICE1234',
        })
        self.assertFalse(form.is_valid())

    def test_form_displays_correct_error_message_if_username_is_not_available(self):
        response = self.client.post(self.view_url, {
            'username' : 'john',
            'email'    : 'alice@mail.com',
            'password1': 'alice1234',
            'password2': 'alice1234',
        })
        self.assertFormError(response,
            'form', 'username', 'User with that username already exists'
        )

    def test_form_displays_correct_error_message_if_email_is_not_available(self):
        response = self.client.post(self.view_url, {
            'username' : 'alice',
            'email'    : 'john@mail.com',
            'password1': 'alice1234',
            'password2': 'alice1234',
         })
        self.assertFormError(response,
            'form', 'email', 'User with that email already exists'
        )

    def test_form_displays_correct_error_message_if_passwords_dont_match(self):
        response = self.client.post(self.view_url, {
            'username' : 'alice',
            'email'    : 'alice@mail.com',
            'password1': 'alice1234',
            'password2': 'ALICE1234',
         })
        self.assertFormError(response,
            'form', 'password2', "Passwords don't match"
        )
