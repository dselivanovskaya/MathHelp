from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic.base import TemplateView

from .apps import AccountsConfig as accounts_config
from .decorators import anonymous_required
from .forms import (
    AccountLoginForm, AccountCreateForm,
    AccountPasswordChangeForm, AccountUsernameChangeForm,
)


@method_decorator(anonymous_required, name='dispatch')
class AccountLoginView(View):

    form_class = AccountLoginForm
    template_name = f'{accounts_config.name}/account-login.html'

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect(settings.LOGIN_REDIRECT_URL)
        return render(request, self.template_name, {'form': form})


@method_decorator(login_required(redirect_field_name=None), name='dispatch')
class AccountLogoutView(View):

    messages = {
        'success': 'Вы вышли из системы.'
    }

    def get(self, request):
        logout(request)
        messages.success(request, self.messages['success'])
        return redirect(settings.INDEX_URL)


@method_decorator(anonymous_required, name='dispatch')
class AccountCreateView(View):

    template_name = f'{accounts_config.name}/account-create.html'
    form_class = AccountCreateForm

    messages = {
        'success': 'Пользователь был успешно создан.'
    }

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, self.messages['success'])
            return redirect(settings.LOGIN_URL)
        return render(request, self.template_name, {'form': form})


@method_decorator(login_required(redirect_field_name=None), name='dispatch')
class AccountSettingsView(TemplateView):

    template_name = f'{accounts_config.name}/account-settings.html'


@method_decorator(login_required(redirect_field_name=None), name='dispatch')
class AccountDeleteView(View):

    template_name = f'{accounts_config.name}/account-delete.html'

    messages = {
        'success': 'Ваш аккаунт был успешно удалён.',
    }

    def get(self, request):
        return render(request, self.template_name, {})

    def post(self, request):
        get_user_model().objects.get(id=request.user.id).delete()
        messages.success(request, self.messages['success'])
        return redirect(settings.INDEX_URL)


@method_decorator(login_required(redirect_field_name=None), name='dispatch')
class AccountPasswordChangeView(View):

    template_name = f'{accounts_config.name}/account-password-change.html'
    form_class = AccountPasswordChangeForm

    messages = {
        'success': 'Пароль был успешно изменён.'
    }

    def get(self, request):
        form = self.form_class(user=request.user)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, self.messages['success'])
            return redirect(accounts_config.ACCOUNT_SETTINGS_URL)
        return render(request, self.template_name, {'form': form})


@method_decorator(login_required(redirect_field_name=None), name='dispatch')
class AccountUsernameChangeView(View):

    template_name = f'{accounts_config.name}/account-username-change.html'
    form_class = AccountUsernameChangeForm

    messages = {
        'success': 'Имя пользователя было успешно изменено.'
    }

    def get(self, request):
        form = self.form_class(user=request.user)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, self.messages['success'])
            return redirect(accounts_config.ACCOUNT_SETTINGS_URL)
        return render(request, self.template_name, {'form': form})
