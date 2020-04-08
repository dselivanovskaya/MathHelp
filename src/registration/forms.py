from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ValidationError


class SignUpForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username',
                  'email', 'password1', 'password2']

    def clean_username(self):
        ''' Check if username already exists. '''
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError('User with that username already exists.')
        return username

    def clean_email(self):
        ''' Check if email already exists. '''
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError('User with that email already exists.')
        return email

