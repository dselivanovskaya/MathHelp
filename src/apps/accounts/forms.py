from django import forms
from django.contrib import auth


class AccountLoginForm(auth.forms.AuthenticationForm):

    error_messages = {
        'invalid_login': 'Неправильное имя пользователя или пароль.',
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.use_required_attribute = False
        self.fields['username'].widget.attrs.pop("autofocus", None)


class AccountCreateForm(auth.forms.UserCreationForm):

    first_name = forms.CharField(max_length=128, widget=forms.TextInput(
        attrs={'placeholder': 'Harry'},
    ))
    last_name = forms.CharField(max_length=128, widget=forms.TextInput(
        attrs={'placeholder': 'Potter'},
    ))
    email = forms.EmailField(max_length=128, widget=forms.EmailInput(
        attrs={'placeholder': 'harry_potter@hogwarts.com'},
    ))
    username = forms.CharField(max_length=128, widget=forms.TextInput(
        attrs={'placeholder': 'harry_potter'},
    ))

    field_order = ('first_name', 'last_name', 'email')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.use_required_attribute = False
        self.fields['username'].widget.attrs.pop("autofocus", None)

    def save(self):
        user = super().save()

        user.email = self.cleaned_data.get('email')
        user.save()

        user.profile.first_name = self.cleaned_data.get('first_name')
        user.profile.last_name = self.cleaned_data.get('last_name')
        user.profile.save()

        return user


class AccountPasswordChangeForm(auth.forms.PasswordChangeForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.use_required_attribute = False
