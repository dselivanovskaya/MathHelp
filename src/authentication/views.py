from django.contrib.auth import login, logout
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import redirect, render, reverse

from .forms import LoginForm


@user_passes_test(lambda user: user.is_anonymous, '/', None)
def login_user(request):
    ''' Log in user. '''

    if request.method == 'GET':
        form = LoginForm()

    elif request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            user = form.cleaned_data['user']
            login(request, user)
            return redirect(reverse('user-profile', args=[user.username]))

    return render(request, 'authentication/login.html', {'form': form})


def logout_user(request):
    ''' Log out user. '''
    logout(request)
    return redirect(reverse('home'))
