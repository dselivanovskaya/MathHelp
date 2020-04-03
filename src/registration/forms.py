from django import forms
from django.forms import ValidationError
from django.contrib.auth.models import User

from .constants import *

# TODO create validators for not available username email and password
# validators.
# https://docs.djangoproject.com/en/3.0/ref/validators/

class RegistrationForm(forms.Form):
    ''' This form is displayed to user when he clicks on register link. '''

    username = forms.CharField(
        label      = 'Username',
        max_length = USERNAME_MAX_LENGTH,
        error_messages = {
            'required'  : USERNAME_REQUIRED,
            'max_length': USERNAME_TOO_LONG,
        }
    )

    email = forms.EmailField(
        label      = 'Email',
        max_length = EMAIL_MAX_LENGTH,
        help_text  = 'Valid email address',
        error_messages = {
            'required'  : EMAIL_REQUIRED,
            'invalid'   : EMAIL_INVALID,
            'max_length': EMAIL_TOO_LONG,
        }
    )

    password = forms.CharField(
        label      = 'Password',
        widget     = forms.PasswordInput(),
        min_length = PASSWORD_MIN_LENGTH,
        max_length = PASSWORD_MAX_LENGTH,
        help_text  = f'{PASSWORD_MIN_LENGTH} characters min.',
        # validators = None,
        error_messages = {
            'required'  : PASSWORD_REQUIRED,
            'min_length': PASSWORD_TOO_SHORT,
            'max_length': PASSWORD_TOO_LONG,
        },
    )

    password2 = forms.CharField(
        label      = 'Repeat password',
        widget     = forms.PasswordInput(),
        min_length = PASSWORD_MIN_LENGTH,
        max_length = PASSWORD_MAX_LENGTH,
        help_text  = f'{PASSWORD_MIN_LENGTH} characters min.',
        # validators = None,
        error_messages = {
            'required'  : PASSWORD_REQUIRED,
            'min_length': PASSWORD_TOO_SHORT,
            'max_length': PASSWORD_TOO_LONG,
        },
    )

    def clean(self):
        ''' This method is called when you check 'if form.is_valid()'. '''
        cleaned_data = super().clean()

        username  = self.cleaned_data.get('username')
        email     = self.cleaned_data.get('email')
        password  = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')

        # If user with 'username' already exists
        if User.objects.filter(username=username).exists():
            raise ValidationError(USERNAME_NOT_AVAILABLE)

        # If user with 'email' already exists
        if User.objects.filter(email=email).exists():
            raise ValidationError(EMAIL_NOT_AVAILABLE)

        # If passwords don't match
        if password and password2 and password != password2:
            raise ValidationError(PASSWORDS_DONT_MATCH)
