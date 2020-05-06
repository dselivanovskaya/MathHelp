from django.forms import ModelForm

from django.core.exceptions import ValidationError
from django.core.files.images import get_image_dimensions

from .models import Profile


class ProfileUpdateForm(ModelForm):

    error_messages = {
        'invalid_photo_size': \
            f'Максимальный размер фото {Profile.get_max_photo_size_display()}.'
    }

    class Meta:
        model = Profile
        exclude = ['user', 'login_count']
        labels = {
            'first_name': 'Имя',
            'last_name':  'Фамилия',
            'photo':      'Фото',
            'gender':     'Пол',
            'age':        'Возраст',
        }

    def clean_photo(self):
        ''' Validate photo size. '''
        photo = self.cleaned_data.get('photo')
        # If user uploads a new image
        if photo != self.instance.photo:
            # Check uploaded photo dimension
            width, height = get_image_dimensions(photo)
            if width > Profile.PHOTO_MAX_WIDTH or height > Profile.PHOTO_MAX_HEIGHT:
                raise ValidationError(self.error_messages['invalid_photo_size'])
            if self.instance.has_uploaded_photo():
                self.instance.delete_photo()
        return photo
