from django.contrib.auth.models import User
from django.test import TestCase

from authentication.forms import SignInForm


class SignInFormTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.view_url = '/sign-in'
        User.objects.create_user(
            username='john', email='john@mail.com', password='johny123'
        )

    def test_form_is_valid_if_user_exists(self):
        form = SignInForm({'username': 'john', 'passsword': 'johny123'})
        self.assertFalse(form.is_valid())

    def test_form_is_invalid_if_user_doesnt_exist(self):
        form = SignInForm({'username': 'alice', 'passsword': 'alice123'})
        self.assertFalse(form.is_valid())

    def test_form_displays_correct_error_message_if_user_doesnt_exist(self):
        response = self.client.post(self.view_url,
            {'username': 'alice', 'password': 'alice123'}
        )
        self.assertFormError(response, 'form', None, 'Invalid username or password')
