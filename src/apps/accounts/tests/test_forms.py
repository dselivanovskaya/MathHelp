from django.conf import settings
from django.shortcuts import reverse
from django.test import TestCase

from tests.data import USER_MALE

from accounts.apps import AccountsConfig
from accounts.forms import AccountLoginForm, AccountCreateForm
from accounts.validators import CustomPasswordValidator


class AccountLoginFormTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.view_url = reverse(AccountsConfig.ACCOUNT_LOGIN_URL)
        cls.form_class = AccountLoginForm

    def test_form_displays_correct_error_message_if_user_doesnt_exist(self):
        response = self.client.post(self.view_url, {
            'username': USER_MALE.username,
            'password': USER_MALE.password,
        })
        self.assertFormError(
            response, 'form', None,
            self.form_class.error_messages['invalid_login']
        )


class AccountCreateFormTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.view_url = reverse(AccountsConfig.ACCOUNT_CREATE_URL)
        cls.form_class = AccountCreateForm
        cls.validator_class = CustomPasswordValidator

    def test_form_is_invalid_if_password_doesnt_have_one_digit(self):
        form = self.form_class({
            'first_name': USER_MALE.first_name,
            'last_name':  USER_MALE.last_name,
            'email':      USER_MALE.email,
            'username':   USER_MALE.username,
            'password1':  'nodigitshere',
            'password2':  'nodigitshere',
        })
        self.assertFalse(form.is_valid())

    def test_form_is_invalid_if_password_doesnt_have_special_character(self):
        form = self.form_class({
            'first_name': USER_MALE.first_name,
            'last_name':  USER_MALE.last_name,
            'email':      USER_MALE.email,
            'username':   USER_MALE.username,
            'password1': 'nospecialcharactershere123',
            'password2': 'nospecialcharactershere123',
        })
        self.assertFalse(form.is_valid())

    def test_form_displays_correct_error_message_if_password_doesnt_have_one_digit(self):
        response = self.client.post(self.view_url, {
            'first_name': USER_MALE.first_name,
            'last_name':  USER_MALE.last_name,
            'email':      USER_MALE.email,
            'username':   USER_MALE.username,
            'password1':  'nodigitshere',
            'password2':  'nodigitshere',
        })
        self.assertFormError(
            response, 'form', 'password2',
            self.validator_class.error_messages['digit']
        )

    def test_form_displays_correct_error_message_if_password_doesnt_have_one_special_character(self):
        response = self.client.post(self.view_url, {
            'first_name': USER_MALE.first_name,
            'last_name':  USER_MALE.last_name,
            'email':      USER_MALE.email,
            'username':   USER_MALE.username,
            'password1': 'nospecialcharactershere123',
            'password2': 'nospecialcharactershere123',
        })
        self.assertFormError(
            response, 'form', 'password2',
            self.validator_class.error_messages['special_char']
        )
