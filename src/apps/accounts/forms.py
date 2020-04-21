from django import forms
from django.contrib import auth
from django.contrib.auth import get_user_model


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

        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.email = self.cleaned_data.get('email')

        user.save()
        return user


class AccountUsernameChangeForm(forms.Form):

    new_username = forms.CharField(max_length=128)

    error_messages = {
        'invalid_new_username': 'Пользователь с таким именем уже существует.'
    }

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)
        self.use_required_attribute = False

    def clean_new_username(self):
        new_username = self.cleaned_data.get('new_username')
        if get_user_model().objects.filter(username=new_username).exists():
            raise forms.ValidationError(
                self.error_messages['invalid_new_username']
            )
        return new_username

    def save(self):
        new_username = self.cleaned_data.get('new_username')
        self.user.username = new_username
        self.user.save()
        return self.user


class AccountPasswordChangeForm(auth.forms.PasswordChangeForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.use_required_attribute = False
