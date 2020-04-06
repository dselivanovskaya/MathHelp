from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.forms import ValidationError


class RegistrationForm(forms.Form):
    ''' Form for user registration. '''

    PASSWORD_MIN_LENGTH = 8

    username = forms.CharField(
        label='Username', max_length=64,
        widget=forms.TextInput(attrs={
            'placeholder': 'example',
        })
    )
    email = forms.EmailField(
        label='Email', max_length=128,
        widget=forms.TextInput(attrs={
            'placeholder': 'example@gmail.com',
        })
    )
    password1 = forms.CharField(
        label='Password', min_length=PASSWORD_MIN_LENGTH, max_length=64,
        widget=forms.PasswordInput(),
        help_text=f'{PASSWORD_MIN_LENGTH} characters min.',
        validators=[validate_password]
    )
    password2 = forms.CharField(
        label='Repeat password', min_length=PASSWORD_MIN_LENGTH, max_length=64,
        widget=forms.PasswordInput(),
        help_text=f'{PASSWORD_MIN_LENGTH} characters min.',
        validators=[validate_password]
    )

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

    def clean_password2(self):
        ''' Check if passwords don't match. '''
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match.")

        return password2
