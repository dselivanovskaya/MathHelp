from django import forms

class ProfileUpdateForm(forms.Form):

    username = forms.CharField(
        required = False,
        label = 'Username',
        max_length = 32,
        error_messages = {
            "required": "Please enter your username :)",
            "invalid": "Please enter a valid username :("
        }
    )

    email = forms.EmailField(
        required = False,
        label = "Email",
        max_length = 32,
        error_messages = {
            "required": "Please enter your email address :)",
            "invalid": "Please enter a valid email address :(",
        }
    )

    password = forms.CharField(
        required = False,
        label = "Password",
        max_length = 32,
        widget = forms.PasswordInput(),
        error_messages = {
            "required": "Please enter your password :)",
            "invalid": "Please enter a valid password :(",
        },
    )
