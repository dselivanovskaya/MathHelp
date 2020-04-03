from django.test import TestCase
from django.contrib.auth.models import User

from profiles.constants import MALE, FEMALE

from .constants import *


class RegisterTestCase(TestCase):

    def setUp(self):
        ''' Create a new user. '''

        self.register_url = '/register/'
        self.username1    = 'alice'
        self.email1       = 'alice@mail.com'
        self.password1    = 'aliceRules11'
        User.objects.create_user(username=self.username1,
                                 email=self.email1,
                                 password=self.password1)
        # Credentials for a new regestering user
        self.username2    = 'new'
        self.email2       = 'new@mail.com'
        self.password2    = 'new12345'

    def test_register_url_exists(self):
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)

    def test_new_user_successful_registration_redirects_to_his_profile(self):
        response = self.client.post(self.register_url,
                    {'username' : self.username2,
                     'email'    : self.email2,
                     'password' : self.password2,
                     'password2': self.password2,
                     })
        self.assertRedirects(response, f'/{self.username2}')

    def test_registration_fails_if_username_field_is_empty(self):
        response = self.client.post(self.register_url,
                    {'username' : '',
                     'email'    : self.email2,
                     'password' : self.password2,
                     'passwordw': self.password2,
                    })
        self.assertFormError(response, 'form', 'username', USERNAME_REQUIRED_ERROR_MESSAGE)

    def test_new_user_registration_fails_if_username_is_too_long(self):
        response = self.client.post(self.register_url,
                    {'username' : 'a' * (USERNAME_MAX_LENGTH + 1),
                     'email'    : self.email2,
                     'password' : self.password2,
                     'passwordw': self.password2,
                    })
        self.assertFormError(response, 'form', 'username', USERNAME_TOO_LONG_ERROR_MESSAGE)

    def test_new_user_registration_fails_if_username_is_not_available(self):
        response = self.client.post(self.register_url,
                    {'username' : self.username1,
                     'email'    : self.email2,
                     'password' : self.password2,
                     'password2': self.password2,
                     })
        self.assertFormError(response, 'form', None, USERNAME_NOT_AVAILABLE_ERROR_MESSAGE)

    def test_new_user_registration_fails_if_email_field_is_empty(self):
        response = self.client.post(self.register_url,
                    {'username' : self.username2,
                     'email'    : '',
                     'password' : self.password2,
                     'password2': self.password2,
                     })
        self.assertFormError(response, 'form', 'email', EMAIL_REQUIRED_ERROR_MESSAGE)

    def test_registration_fails_if_email_field_is_invalid(self):
        response = self.client.post(self.register_url,
                    {'username' : self.username2,
                     'email'    : 'abcde',
                     'password' : self.password2,
                     'password2': self.password2
                    })
        self.assertFormError(response, 'form', 'email', EMAIL_INVALID_ERROR_MESSAGE)

    def test_new_user_registration_fails_if_email_is_too_long(self):
        response = self.client.post(self.register_url,
                    {'username' : self.username2,
                     'email'    : 'a' * (EMAIL_MAX_LENGTH) + '@mail.com',
                     'password' : self.password2,
                     'passwordw': self.password2,
                    })
        self.assertFormError(response, 'form', 'email', EMAIL_TOO_LONG_ERROR_MESSAGE)

    def test_new_user_registration_fails_if_email_is_not_available(self):
        response = self.client.post(self.register_url,
                    {'username' : self.username2,
                     'email'    : self.email1,
                     'password' : self.password2,
                     'password2': self.password2,
                     })
        self.assertFormError(response, 'form', None, EMAIL_NOT_AVAILABLE_ERROR_MESSAGE)

    def test_registration_fails_if_password_field_is_empty(self):
        response = self.client.post(self.register_url,
                    {'username' : self.username2,
                     'email'    : self.email2,
                     'password' : '',
                     'password2': self.password2,
                    })
        self.assertFormError(response, 'form', 'password', PASSWORD_REQUIRED_ERROR_MESSAGE)

    def test_registration_fails_if_password_repeat_field_is_empty(self):
        response = self.client.post(self.register_url,
                    {'username' : self.username2,
                     'email'    : self.email2,
                     'password' : self.password2,
                     'password2': '',
                    })
        self.assertFormError(response, 'form', 'password2', PASSWORD_REQUIRED_ERROR_MESSAGE)

    def test_registration_fails_if_password_field_password_is_too_short(self):
        response = self.client.post(self.register_url,
                    {'username' : self.username2,
                     'email'    : self.email2,
                     'password' : '12',
                     'password2': '12',
                    })
        self.assertFormError(response, 'form', 'password', PASSWORD_TOO_SHORT_ERROR_MESSAGE)

    def test_registration_fails_if_password_field_password_is_too_long(self):
        response = self.client.post(self.register_url,
                    {'username'  : self.username2,
                     'email'     : self.email2,
                     'password'  : 'a' * (PASSWORD_MAX_LENGTH + 1),
                     'password2' : 'a' * (PASSWORD_MAX_LENGTH + 1),
                    })
        self.assertFormError(response, 'form', 'password', PASSWORD_TOO_LONG_ERROR_MESSAGE)

    def test_new_user_registration_fails_if_password_fields_not_match(self):
        response = self.client.post(self.register_url,
                    {'username' : self.username2,
                     'email'    : self.email2,
                     'password' : self.password1,
                     'password2': self.password2,
                    })
        self.assertFormError(response, 'form', None, PASSWORDS_NOT_MATCH_ERROR_MESSAGE)
