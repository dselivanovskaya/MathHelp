from django import forms

from .constants import (USERNAME_REQUIRED_ERROR_MESSAGE,
                        EMAIL_REQUIRED_ERROR_MESSAGE,
                        PASSWORD_REQUIRED_ERROR_MESSAGE,
                        EMAIL_INVALID_ERROR_MESSAGE)


class UserRegistrationForm(forms.Form):

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
