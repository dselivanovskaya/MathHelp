from django.conf import settings

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin

from django.urls import reverse_lazy
from django.utils.decorators import method_decorator

from django.views.generic.edit import CreateView, UpdateView, DeleteView

from .apps import AccountsConfig
from .decorators import anonymous_required
from .forms import AccountLoginForm, AccountCreateForm, AccountPasswordChangeForm


class AccountLoginView(LoginView):

    form_class = AccountLoginForm
    template_name = f'{AccountsConfig.name}/account-login.html'
    redirect_authenticated_user = True


class AccountLogoutView(LogoutView):
    pass  # Consistency :)


@method_decorator(anonymous_required, name='dispatch')
class AccountCreateView(SuccessMessageMixin, CreateView):

    form_class = AccountCreateForm
    template_name = f'{AccountsConfig.name}/account-create.html'
    success_url = reverse_lazy(settings.LOGIN_URL)
    success_message = 'Пользователь был успешно создан.'


class AccountDeleteView(DeleteView):

    model = get_user_model()
    template_name = f'{AccountsConfig.name}/account-confirm-delete.html'
    success_url = reverse_lazy(settings.INDEX_URL)
    success_message = "Ваш аккаунт был успешно удалён."

    def get_object(self):
        return self.request.user

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)


class AccountPasswordChangeView(SuccessMessageMixin, PasswordChangeView):

    form_class = AccountPasswordChangeForm
    template_name = f'{AccountsConfig.name}/account-password-change.html'
    success_url = reverse_lazy(settings.LOGIN_REDIRECT_URL)
    success_message = 'Пароль был успешно изменён.'


class AccountUsernameUpdateView(SuccessMessageMixin, UpdateView):

    model = get_user_model()
    fields = ['username']
    template_name = f'{AccountsConfig.name}/account-username-update.html'
    success_url = reverse_lazy(settings.LOGIN_REDIRECT_URL)
    success_message = 'Имя пользователя было успешно изменено.'

    def get_object(self):
        return self.request.user


class AccountEmailUpdateView(SuccessMessageMixin, UpdateView):

    model = get_user_model()
    fields = ['email']
    template_name = f'{AccountsConfig.name}/account-email-update.html'
    success_url = reverse_lazy(settings.LOGIN_REDIRECT_URL)
    success_message = 'Адрес электронной почты был успешно изменён.'

    def get_object(self):
        return self.request.user
