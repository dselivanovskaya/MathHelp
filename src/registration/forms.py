from django import forms

from profiles.models import Profile


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
        choices = Profile.GENDER_CHOICES
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
        min_length = 8,
        widget = forms.PasswordInput(),
        error_messages = {
            "required": "Please enter your password :)",
            "invalid": "Please enter a valid password :(",
            "min_length": "Password must be at least 8 characters long :(",
            #"max_length": "Password can be at most 32 characters long :(",
        },
    )
