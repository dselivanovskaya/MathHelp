from django import forms
from django.forms import ValidationError
from django.contrib.auth.models import User

from .constants import *


class RegistrationForm(forms.Form):

    username = forms.CharField(
        required = True,
        label = 'Username',
        max_length = 32,
        error_messages = {
            'required': USERNAME_REQUIRED_ERROR_MESSAGE,
            'invalid': 'Please enter a valid username :('
        }
    )

    email = forms.EmailField(
        required = True,
        label = 'Email',
        max_length = 32,
        error_messages = {
            'required': EMAIL_REQUIRED_ERROR_MESSAGE,
            'invalid' : EMAIL_INVALID_ERROR_MESSAGE,
        }
    )

    password = forms.CharField(
        required = True,
        label = 'Password',
        max_length = 32,
        widget = forms.PasswordInput(),
        error_messages = {
            'required': PASSWORD_REQUIRED_ERROR_MESSAGE,
            'invalid': 'Please enter a valid password :(',
        },
    )

    password2 = forms.CharField(
        required = True,
        label = 'Repeat password',
        max_length = 32,
        widget = forms.PasswordInput(),
        error_messages = {
            'required': PASSWORD_REQUIRED_ERROR_MESSAGE,
            'invalid': 'Please enter a valid password :(',
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
            raise ValidationError(USERNAME_NOT_AVAILABLE_ERROR_MESSAGE)

        # If user with 'email' already exists
        if User.objects.filter(email=email).exists():
            raise ValidationError(EMAIL_NOT_AVAILABLE_ERROR_MESSAGE)

        # If passwords don't match
        if password and password2 and password != password2:
            raise ValidationError(PASSWORDS_NOT_MATCH_ERROR_MESSAGE)
