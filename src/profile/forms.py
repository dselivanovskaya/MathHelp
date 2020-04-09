from django.forms import ModelForm
from django import forms

from .models import Profile


class UpdateProfileForm(ModelForm):

    first_name = forms.CharField(max_length=64, min_length=1, required=False)
    last_name = forms.CharField(max_length=64, min_length=1, required=False)

    class Meta:
        model = Profile
        fields = ['gender', 'age']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs);
        self.use_required_attribute = False

    def save(self, *args, **kwargs):
        profile = super().save(*args, **kwargs)

        first_name = self.cleaned_data.get('first_name')
        last_name = self.cleaned_data.get('last_name')

        if first_name:
            profile.user.first_name = first_name
        if last_name:
            profile.user.last_name = last_name

        profile.user.save()
