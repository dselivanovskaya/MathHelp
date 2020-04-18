from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, logout
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views import View

from .apps import AccountsConfig
from .decorators import anonymous_required
from .forms import SigninForm, SignupForm


@method_decorator(anonymous_required, name='dispatch')
class SigninView(View):

    form_class = SigninForm
    template_name = f'{AccountsConfig.name}/signin.html'

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect(settings.LOGIN_REDIRECT_URL)
        return render(request, self.template_name, {'form': form})


@method_decorator(anonymous_required, name='dispatch')
class SignupView(View):

    template_name = f'{AccountsConfig.name}/signup.html'
    form_class = SignupForm

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(data=request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f'User {user.username} has been created.')
            return redirect(settings.LOGIN_URL)
        return render(request, self.template_name, {'form': form})


class SignoutView(View):

    def get(self, request):
        logout(request)
        return redirect(settings.LOGOUT_REDIRECT_URL)
