from django import forms
from django.contrib import auth


class SigninForm(auth.forms.AuthenticationForm):

    error_messages = {
        'invalid_login': 'Incorrect username or password.',
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.use_required_attribute = False
        self.fields['username'].widget.attrs.pop("autofocus", None)


class SignupForm(auth.forms.UserCreationForm):

    full_name = forms.CharField(max_length=255, widget=forms.TextInput(
        attrs={'placeholder': 'Harry Potter'},
    ))
    email = forms.EmailField(max_length=255, widget=forms.EmailInput(
        attrs={'placeholder': 'harry_potter@hogwarts.com'},
    ))
    username = forms.CharField(max_length=128, widget=forms.TextInput(
        attrs={'placeholder': 'harry_potter'},
    ))

    field_order = ('full_name', 'email')

    error_messages = {
        'invalid_full_name': 'Invalid full name.',
        'password_mismatch': 'The two password fields didn’t match.',
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.use_required_attribute = False
        self.fields['username'].widget.attrs.pop("autofocus", None)

    def clean_full_name(self):
        full_name = self.cleaned_data.get('full_name')
        if len(full_name.split()) != 2:
            raise forms.ValidationError(
                self.error_messages['invalid_full_name']
            )
        return full_name

    def save(self):
        user = super().save()
        first_name, last_name = self.cleaned_data.get('full_name').split()
        user.first_name, user.last_name = first_name, last_name
        user.email = self.cleaned_data.get('email')
        user.save()
        return user
