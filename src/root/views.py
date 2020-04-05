from django.contrib.auth import login, logout
from django.shortcuts import redirect, render, reverse

from .forms import LoginForm


def login_user(request):
    ''' Log in user. '''
    # Redirect already logged-in users to their profiles.
    if request.user.is_authenticated:
        return redirect(reverse('show-user-profile',
            kwargs={'username': request.user.username}
        ))

    if request.method == 'GET':
        form = LoginForm()

    elif request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():

            user = form.cleaned_data['user']
            login(request, user)

            user.profile.login_count += 1
            user.save()

            return redirect(
                reverse('show-user-profile', kwargs={'username': user.username})
            )

    return render(request, 'root/login.html', {'form': form})


def logout_user(request):
    ''' Log out user. '''
    logout(request)
    return redirect(reverse('home'))
