from django.contrib.auth.models import User
from django.test import TestCase

from registration.forms import RegistrationForm


class RegistrationFormTest(TestCase):
    ''' Tests for RegistrationForm. '''

    JOHN_USERNAME = 'john'
    JOHN_EMAIL = 'john@mail.com'
    JOHN_PASSWORD = 'John_123'

    ALICE_USERNAME = 'alice'
    ALICE_EMAIL = 'alice@gmail.com'
    ALICE_PASSOWRD = 'Alice_123'

    @classmethod
    def setUpTestData(cls):
        cls.view_url = '/register/'
        User.objects.create_user(
            username=cls.JOHN_USERNAME,
            email=cls.JOHN_EMAIL,
            password=cls.JOHN_PASSWORD
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

    def test_password_fields_help_text(self):
        form = RegistrationForm()
        self.assertEqual(form.fields['password1'].help_text,
            f'{RegistrationForm.PASSWORD_MIN_LENGTH} characters min.'
        )
        self.assertEqual(form.fields['password2'].help_text,
            f'{RegistrationForm.PASSWORD_MIN_LENGTH} characters min.'
        )

    def test_form_is_invalid_if_username_is_not_available(self):
        form = RegistrationForm({
            'username' : self.JOHN_USERNAME,
            'email'    : self.ALICE_EMAIL,
            'password1': self.ALICE_PASSOWRD,
            'password2': self.ALICE_PASSOWRD,
        })
        self.assertFalse(form.is_valid())

    def test_form_is_invalid_if_email_is_not_available(self):
        form = RegistrationForm({
            'username' : self.ALICE_USERNAME,
            'email'    : self.JOHN_EMAIL,
            'password1': self.ALICE_PASSOWRD,
            'password2': self.ALICE_PASSOWRD,
        })
        self.assertFalse(form.is_valid())

    def test_form_is_invalid_if_passwords_dont_match(self):
        form = RegistrationForm({
            'username' : self.ALICE_USERNAME,
            'email'    : self.ALICE_EMAIL,
            'password1': self.ALICE_PASSOWRD,
            'password2': self.ALICE_PASSOWRD + '0',
        })
        self.assertFalse(form.is_valid())

    def test_form_is_invalid_if_password_doesnt_have_one_digit(self):
        form = RegistrationForm({
            'username' : self.ALICE_USERNAME,
            'email'    : self.ALICE_EMAIL,
            'password1': 'aliceiscool',
            'password1': 'aliceiscool',
        })
        self.assertFalse(form.is_valid())

    def test_form_is_invalid_if_password_doesnt_have_one_uppercase_letter(self):
        form = RegistrationForm({
            'username' : self.ALICE_USERNAME,
            'email'    : self.ALICE_EMAIL,
            'password1': 'aliceiscool12',
            'password2': 'aliceiscool12',

        })
        self.assertFalse(form.is_valid())

    def test_form_is_invalid_if_password_doesnt_have_one_lowercase_letter(self):
        form = RegistrationForm({
            'username' : self.ALICE_USERNAME,
            'email'    : self.ALICE_EMAIL,
            'password1': 'ALICEISCOOL12',
            'password2': 'ALICEISCOOL12',
        })
        self.assertFalse(form.is_valid())

    def test_form_is_invalid_if_password_doesnt_have_one_special_character(self):
        form = RegistrationForm({
            'username' : self.ALICE_USERNAME,
            'email'    : self.ALICE_EMAIL,
            'password1': 'aliceIsCool12',
            'password2': 'aliceIsCool12',
        })
        self.assertFalse(form.is_valid())

    def test_form_displays_correct_error_message_if_username_is_not_available(self):
        response = self.client.post(self.view_url, {
            'username' : self.JOHN_USERNAME,
            'email'    : self.ALICE_EMAIL,
            'password1': self.ALICE_PASSOWRD,
            'password2': self.ALICE_PASSOWRD,
        })
        self.assertFormError(response,
            'form', 'username', 'User with that username already exists.'
        )

    def test_form_displays_correct_error_message_if_email_is_not_available(self):
        response = self.client.post(self.view_url, {
            'username' : self.ALICE_USERNAME,
            'email'    : self.JOHN_EMAIL,
            'password1': self.ALICE_PASSOWRD,
            'password2': self.ALICE_PASSOWRD,
         })
        self.assertFormError(response,
            'form', 'email', 'User with that email already exists.'
        )

    def test_form_displays_correct_error_message_if_passwords_dont_match(self):
        response = self.client.post(self.view_url, {
            'username' : self.ALICE_USERNAME,
            'email'    : self.ALICE_EMAIL,
            'password1': self.ALICE_PASSOWRD,
            'password2': self.ALICE_PASSOWRD + '0',
         })
        self.assertFormError(response,
            'form', 'password2', "Passwords don't match."
        )

    def test_form_displays_correct_error_message_if_password_doesnt_have_one_digit(self):
        response = self.client.post(self.view_url, {
            'username' : self.ALICE_USERNAME,
            'email'    : self.ALICE_EMAIL,
            'password1': 'aliceiscool',
            'password2': 'aliceiscool',
        })
        self.assertFormError(response,
            'form', 'password2', 'Password must contain at least 1 digit.'
        )

    def test_form_displays_correct_error_message_if_password_doesnt_have_one_uppercase_letter(self):
        response = self.client.post(self.view_url, {
            'username' : self.ALICE_USERNAME,
            'email'    : self.ALICE_EMAIL,
            'password1': 'aliceiscool12',
            'password2': 'aliceiscool12',
        })
        self.assertFormError(response,
            'form', 'password2', 'Password must contain at least 1 uppercase letter.'
        )

    def test_form_displays_correct_error_message_if_password_doesnt_have_one_lowercase_letter(self):
        response = self.client.post(self.view_url, {
            'username' : self.ALICE_USERNAME,
            'email'    : self.ALICE_EMAIL,
            'password1': 'ALICEISCOOL12',
            'password2': 'ALICEISCOOL12',
        })
        self.assertFormError(response,
            'form', 'password2', 'Password must contain at least 1 lowercase letter.'
        )

    def test_form_displays_correct_error_message_if_password_doesnt_have_one_special_character(self):
        response = self.client.post(self.view_url, {
            'username' : self.ALICE_USERNAME,
            'email'    : self.ALICE_EMAIL,
            'password1': 'aliceIsCool12',
            'password2': 'aliceIsCool12',
        })
        self.assertFormError(response,
            'form', 'password2', 'Password must contain at least 1 special character.'
        )
