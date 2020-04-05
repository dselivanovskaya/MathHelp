from django.test import TestCase
from django.contrib.auth.models import User

from registration.forms import UserRegistrationForm


class UserRegistrationFormTest(TestCase):
    ''' Tests for UserRegistrationForm. '''

    @classmethod
    def setUpTestData(cls):
        cls.view_url = '/register/'
        User.objects.create_user(username='john',
                                 email='john@mail.com',
                                 password='johnisthebest12')

    def test_password_field_help_text(self):
        form = UserRegistrationForm()
        self.assertEqual(form.fields['password1'].help_text, '8 characters min.')

    def test_repeat_password_field_help_text(self):
        form = UserRegistrationForm()
        self.assertEqual(form.fields['password2'].help_text, '8 characters min.')

    def test_is_invalid_if_username_not_available(self):
        form = UserRegistrationForm({
                'username' : 'john',
                'email'    : 'smith@mail.com',
                'password1': 'jj12345678',
                'password2': 'jj12345678',
        })
        self.assertFalse(form.is_valid())

    def test_is_invalid_if_email_not_available(self):
        form = UserRegistrationForm({
                'username' : 'smith',
                'email'    : 'john@mail.com',
                'password1': 'jj12345678',
                'password2': 'jj12345678',
        })
        self.assertFalse(form.is_valid())

    def test_is_invalid_if_passwords_dont_match(self):
        form = UserRegistrationForm({
                'username' : 'smith',
                'email'    : 'smith@mail.com',
                'password1': 'jj12345678',
                'password2': 'JJ12345678',
        })
        self.assertFalse(form.is_valid())

    def test_correct_error_message_if_username_not_available(self):
        response = self.client.post(self.view_url,
                    {'username' : 'john',
                     'email'    : 'smith@mail.com',
                     'password1': 'jj12345678',
                     'password2': 'jj12345678',
                     })
        self.assertFormError(response, 'form', 'username',
                             'User with that username already exists')

    def test_correct_error_message_if_email_not_available(self):
        response = self.client.post(self.view_url,
                    {'username' : 'john',
                     'email'    : 'john@mail.com',
                     'password1': 'jj12345678',
                     'password2': 'jj12345678',
                     })
        self.assertFormError(response, 'form', 'email',
                             'User with that email already exists')

    def test_correct_error_message_if_passwords_dont_match(self):
        response = self.client.post(self.view_url,
                    {'username' : 'john',
                     'email'    : 'smith@mail.com',
                     'password1': 'jj12345678',
                     'password2': 'JJ12345678',
                     })
        self.assertFormError(response, 'form', 'password2', "Passwords don't match")
