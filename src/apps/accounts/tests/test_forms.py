from django.conf import settings
from django.shortcuts import reverse
from django.test import TestCase

from tests.data import MALE_USER

from accounts.apps import AccountsConfig
from accounts.forms import AccountLoginForm, AccountCreateForm
from accounts.validators import CustomPasswordValidator


class AccountLoginFormTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.form_class = AccountLoginForm
        cls.action_url = reverse(AccountsConfig.ACCOUNT_LOGIN_URL)

    def test_form_returns_error_if_user_doesnt_exist(self):
        response = self.client.post(self.action_url, {
            'username': MALE_USER.username,
            'password': MALE_USER.password,
        })
        error_message = self.form_class.error_messages['invalid_login']
        self.assertFormError(response, 'form', None, error_message)


class AccountCreateFormTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.form_class = AccountCreateForm
        cls.validator_class = CustomPasswordValidator
        cls.action_url = reverse(AccountsConfig.ACCOUNT_CREATE_URL)

    def test_form_is_invalid_if_password_doesnt_have_one_digit(self):
        form = self.form_class({
            'first_name': MALE_USER.first_name,
            'last_name':  MALE_USER.last_name,
            'email':      MALE_USER.email,
            'username':   MALE_USER.username,
            'password1':  'nodigitshere',
            'password2':  'nodigitshere',
        })
        self.assertFalse(form.is_valid())

    def test_form_is_invalid_if_password_doesnt_have_special_character(self):
        form = self.form_class({
            'first_name': MALE_USER.first_name,
            'last_name':  MALE_USER.last_name,
            'email':      MALE_USER.email,
            'username':   MALE_USER.username,
            'password1': 'nospecialcharactershere123',
            'password2': 'nospecialcharactershere123',
        })
        self.assertFalse(form.is_valid())

    def test_form_returns_error_if_password_doesnt_have_one_digit(self):
        response = self.client.post(self.action_url, {
            'first_name': MALE_USER.first_name,
            'last_name':  MALE_USER.last_name,
            'email':      MALE_USER.email,
            'username':   MALE_USER.username,
            'password1':  'nodigitshere',
            'password2':  'nodigitshere',
        })
        error_message = self.validator_class.error_messages['digit']
        self.assertFormError(response, 'form', 'password2', error_message)

    def test_form_returns_error_if_password_doesnt_have_one_special_character(self):
        response = self.client.post(self.action_url, {
            'first_name': MALE_USER.first_name,
            'last_name':  MALE_USER.last_name,
            'email':      MALE_USER.email,
            'username':   MALE_USER.username,
            'password1': 'nospecialcharactershere123',
            'password2': 'nospecialcharactershere123',
        })
        error_message = self.validator_class.error_messages['special_char']
        self.assertFormError(response, 'form', 'password2', error_message)
