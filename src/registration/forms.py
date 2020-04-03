from django import forms

from profiles.constants import GENDER_CHOICES


class UserRegistrationForm(forms.Form):

    username = forms.CharField(
        required = True,
        label = 'Username',
        max_length = 32,
        error_messages = {
            "required": "Please enter your username :)",
            "invalid": "Please enter a valid username :("
        }
    )

    gender = forms.ChoiceField(
        choices = GENDER_CHOICES
    )

    email = forms.EmailField(
        required = True,
        label = "Email",
        max_length = 32,
        error_messages = {
            "required": "Please enter your email address :)",
            "invalid": "Please enter a valid email address :(",
        }
    )

    password = forms.CharField(
        required = True,
        label = "Password",
        max_length = 32,
        widget = forms.PasswordInput(),
        error_messages = {
            "required": "Please enter your password :)",
            "invalid": "Please enter a valid password :(",
        },
    )
