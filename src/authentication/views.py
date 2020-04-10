from django.contrib.auth import login, logout
from django.shortcuts import redirect, render, reverse
from django.views import View
from django.utils.decorators import method_decorator

from .forms import SignInForm
from .decorators import anonymous_required


@method_decorator(anonymous_required, name='dispatch')
class SignInView(View):

    form_class = SignInForm
    template_name = 'authentication/sign-in.html'

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.cleaned_data['user']
            login(request, user)
            request.session['watched_tickets'] = []
            return redirect(reverse('profile'))
        return render(request, self.template_name, {'form': form})


class SignOutView(View):

    def get(self, request):
        logout(request)
        return redirect(reverse('home'))
