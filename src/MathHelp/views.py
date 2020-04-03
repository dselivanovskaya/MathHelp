from django.shortcuts import redirect, render, reverse

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm

from .constants import FAIL_LOGIN_ERROR_MESSAGE


def login_user(request):
    ''' Log in user. '''

    # Redirect already logged-in users to their profiles.
    if request.user.is_active:
        return redirect(reverse('show-user-profile', kwargs={
                   'username': request.user.username
               }))

    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)

        if not form.is_valid():
            messages.error(request, FAIL_LOGIN_ERROR_MESSAGE)
        else:
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(username=username, password=password)

            if user is None:
                messages.error(request, FAIL_LOGIN_ERROR_MESSAGE)
            else:
                login(request, user)

                user.profile.login_count += 1
                user.profile.save()

                return redirect(reverse('show-user-profile', kwargs={
                           'username': username,
                       }))

    return render(request, 'login.html', {'form': AuthenticationForm})


def logout_user(request):
    ''' Log out user. '''
    logout(request)
    return redirect(reverse('home'))
