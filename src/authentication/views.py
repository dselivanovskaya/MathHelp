from django.contrib.auth import login, logout
from django.shortcuts import redirect, render, reverse

from .forms import SignInForm
from .decorators import anonymous_required


@anonymous_required
def sign_in(request):
    if request.method == 'GET':
        form = SignInForm()

    elif request.method == 'POST':
        form = SignInForm(request.POST)

        if form.is_valid():
            user = form.cleaned_data['user']
            login(request, user)
            request.session['watched_tickets'] = []
            return redirect(reverse('profile'))

    return render(request, 'authentication/sign-in.html', {'form': form})


def sign_out(request):
    logout(request)
    return redirect(reverse('home'))
