from django import forms
from django.contrib.auth import authenticate
from django.forms import ValidationError

class LoginForm(forms.Form):
    ''' Form for user log in. '''

    username = forms.CharField(label='Username')
    password = forms.CharField(label='Password', widget=forms.PasswordInput())

    def clean(self):
        ''' Check if user with 'username' and 'password' exists. '''
        super().clean()

        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        user = authenticate(username=username, password=password)

        if user is None:
            raise ValidationError('Invalid username or password')

        self.cleaned_data['user'] = user
