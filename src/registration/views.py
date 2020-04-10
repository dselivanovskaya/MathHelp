from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render, reverse
from django.utils.decorators import method_decorator
from django.views import View

from authentication.decorators import anonymous_required

from .forms import SignUpForm


@method_decorator(anonymous_required, name='dispatch')
class SignUpView(View):

    form_class = SignUpForm
    template_name = 'registration/registration.html'

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1']
            )
            login(request, user)
            return redirect(reverse('profile'))
        return render(request, self.template_name, {'form': form})
