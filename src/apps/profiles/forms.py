from django import forms
from django.forms import ModelForm

from .models import Profile


class ProfileUpdateForm(ModelForm):

    first_name = forms.CharField(max_length=64, min_length=1, required=False)
    last_name = forms.CharField(max_length=64, min_length=1, required=False)
    email = forms.EmailField(max_length=128, required=False)

    field_order = ('first_name', 'last_name', 'email')

    class Meta:
        model = Profile
        fields = ('gender', 'age')

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)
        self.use_required_attribute = False

    def save(self, *args, **kwargs):
        profile = super().save(*args, **kwargs)

        first_name = self.cleaned_data.get('first_name')
        last_name = self.cleaned_data.get('last_name')
        email = self.cleaned_data.get('email')

        if first_name:
            profile.user.first_name = first_name
        if last_name:
            profile.user.last_name = last_name
        if email:
            profile.user.email = email

        profile.user.save()
        return profile
