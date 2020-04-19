from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm

from .models import Profile


class ProfileUpdateForm(ModelForm):

    first_name = forms.CharField(max_length=64, min_length=1, required=False)
    last_name = forms.CharField(max_length=64, min_length=1, required=False)

    email = forms.EmailField(max_length=128, required=False)
    username = forms.CharField(max_length=128, min_length=1, required=False)

    field_order = ('first_name', 'last_name', 'email', 'username')

    error_messages = {
        'invalid_username': 'A user with that username already exists.',
    }

    class Meta:
        model = Profile
        fields = ('gender', 'age')

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)
        self.use_required_attribute = False

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if username != self.user.username and \
           User.objects.filter(username=username).exists():
            raise forms.ValidationError(self.error_messages['invalid_username'])
        return username

    def save(self, *args, **kwargs):
        profile = super().save(*args, **kwargs)

        first_name = self.cleaned_data.get('first_name')
        last_name = self.cleaned_data.get('last_name')
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')

        if first_name:
            profile.user.first_name = first_name
        if last_name:
            profile.user.last_name = last_name
        if email:
            profile.user.email = email
        if username:
            profile.user.username = username

        profile.user.save()
        return profile
