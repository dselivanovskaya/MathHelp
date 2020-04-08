from PIL import Image

from django.forms import ModelForm

from .models import Profile


class UpdateProfileForm(ModelForm):

    class Meta:
        model = Profile
        fields = ['gender', 'image', 'age', 'first_name', 'last_name']