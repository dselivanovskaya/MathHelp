from django import forms
from django.forms import ModelForm
from django.core.files.images import get_image_dimensions

from .models import Profile


class ProfileUpdateForm(ModelForm):

    first_name = forms.CharField(max_length=64, min_length=1, required=False)
    last_name = forms.CharField(max_length=64, min_length=1, required=False)
    email = forms.EmailField(max_length=128, required=False)

    field_order = ('first_name', 'last_name', 'email')
    error_messages = {
        'invalid_photo_size': (
            'Максимальный размер фотографии '
            f'{Profile.PHOTO_MAX_WIDTH} x {Profile.PHOTO_MAX_HEIGHT} пикселей.'
        )
    }

    class Meta:
        model = Profile
        fields = ('photo', 'gender', 'age')

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)
        self.use_required_attribute = False

    def clean_photo(self):
        photo = self.cleaned_data.get('photo')
        # If user uploads a new image
        if photo != self.user.profile.photo:
            # Check uploaded photo dimension
            width, height = get_image_dimensions(photo)
            if width > Profile.PHOTO_MAX_WIDTH:
                raise forms.ValidationError(
                    self.error_messages['invalid_photo_size']
                )
            if height > Profile.PHOTO_MAX_HEIGHT:
                raise forms.ValidationError(
                    self.error_messages['invalid_photo_size']
                )
            self.user.profile.delete_photo()
        return photo

    def save(self, *args, **kwargs):
        profile = super().save(*args, **kwargs)

        first_name = self.cleaned_data.get('first_name')
        last_name = self.cleaned_data.get('last_name')
        email = self.cleaned_data.get('email')

        changed = False

        if first_name != profile.user.first_name:
            profile.user.first_name = first_name
            changed = True

        if last_name != profile.user.last_name:
            profile.user.last_name = last_name
            changed = True

        if email != profile.user.email:
            profile.user.email = email
            changed = True

        if changed:
            profile.user.save()

        return profile
