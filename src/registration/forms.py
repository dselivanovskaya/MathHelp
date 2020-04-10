from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django import forms


class SignUpForm(UserCreationForm):

    email = forms.EmailField(max_length=128)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs);
        self.use_required_attribute = False
        self.fields['username'].widget.attrs.pop("autofocus", None)

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
