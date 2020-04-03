from django.test import TestCase
from django.contrib.auth.models import User

from profiles.constants import MALE, FEMALE

from .constants import (USERNAME_NOT_AVAILABLE_ERROR_MESSAGE,
                        USERNAME_REQUIRED_ERROR_MESSAGE,
                        EMAIL_REQUIRED_ERROR_MESSAGE,
                        PASSWORD_REQUIRED_ERROR_MESSAGE,
                        EMAIL_INVALID_ERROR_MESSAGE)


class RegisterTestCase(TestCase):

    def setUp(self):
        ''' Create a new user. '''

        self.register_url = '/register/'
        self.username     = 'alice'
        self.email        = 'alice@mail.com'
        self.password     = 'aliceRules11'
        self.user         = User.objects.create_user(username=self.username,
                                                     email=self.email,
                                                     password=self.password)
        # Credentials for a new regestering user
        self.username2    = 'new'
        self.email2       = 'new@mail.com'
        self.password2    = 'new1234'

    def test_register_url_exists(self):
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)

    def test_new_user_successful_registration_redirects_to_his_profile(self):
        response = self.client.post(self.register_url,
                    {'username': self.username2,
                     'email'   : self.email2,
                     'password': self.password2,
                     })
        self.assertRedirects(response, f'/{self.username2}')

    def test_new_user_registration_fails_if_username_is_not_available(self):
        response = self.client.post(self.register_url,
                    {'username': self.username,
                     'email'   : self.email2,
                     'password': self.password2,
                     })
        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), USERNAME_NOT_AVAILABLE_ERROR_MESSAGE)

    def test_new_user_registration_fails_if_email_is_not_available(self):
        response = self.client.post(self.register_url,
                    {'username': self.username2,
                     'email'   : self.email,
                     'password': self.password2
                     })
        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), USERNAME_NOT_AVAILABLE_ERROR_MESSAGE)

    def test_registration_fails_if_username_field_is_empty(self):
        response = self.client.post(self.register_url,
                    {'username': '',
                     'email'   : self.email2,
                     'password': self.password2,
                    })
        self.assertFormError(response, 'form', 'username', USERNAME_REQUIRED_ERROR_MESSAGE)

    def test_new_user_registration_fails_if_email_field_is_empty(self):
        response = self.client.post(self.register_url,
                    {'username': self.username2,
                     'email'   : '',
                     'password': self.password2,
                        })
        self.assertFormError(response, 'form', 'email', EMAIL_REQUIRED_ERROR_MESSAGE)

    def test_registration_fails_if_password_field_is_empty(self):
        response = self.client.post(self.register_url,
                    {'username': self.username2,
                     'email'   : self.email2,
                     'password': ''
                    })
        self.assertFormError(response, 'form', 'password', PASSWORD_REQUIRED_ERROR_MESSAGE)

    def test_registration_fails_if_email_field_is_invalid(self):
        response = self.client.post(self.register_url,
                    {'username': self.username2,
                     'email'   : 'abcde',
                     'password': self.password2
                    })
        self.assertFormError(response, 'form', 'email', EMAIL_INVALID_ERROR_MESSAGE)


