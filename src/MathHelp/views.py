from django.shortcuts import redirect, render, reverse

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm

from django.contrib.auth.models import User


def login_request(request):
    """ Log in user. """
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                user_profile = User.objects.get(id=user.id).profile
                user_profile.login_count += 1
                user_profile.save()
                return redirect(reverse('show-user-profile', kwargs={'username':username}))
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})


def logout_request(request):
    """ Log out user. """
    logout(request)
    return redirect(reverse('home'))

