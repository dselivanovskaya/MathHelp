from django import forms
from django.contrib.auth import authenticate
from django.forms import ValidationError


class LoginForm(forms.Form):
    ''' This form is displayed to logging in users. '''

    username = forms.CharField(label='Username')
    password = forms.CharField(label='Password', widget=forms.PasswordInput())

    def clean(self):
        ''' Check if user with 'username' and 'password' exists. '''
        super().clean()

        user = authenticate(
            username=self.cleaned_data.get('username'),
            password=self.cleaned_data.get('password'),
        )

        if user is None:
            raise ValidationError('Invalid username or password')

        self.cleaned_data['user'] = user
