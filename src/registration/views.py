from django.shortcuts import render, redirect, reverse

from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User

from .forms import RegistrationForm


def register_user(request):

    if request.method == 'GET':
        form = RegistrationForm()

    elif request.method == 'POST':
        form = RegistrationForm(request.POST)

        if form.is_valid():

            username = form.cleaned_data['username']
            email    = form.cleaned_data['email']
            password = form.cleaned_data['password']

            # Create user
            user = User.objects.create_user(username, email, password)
            # Login user
            user = authenticate(username=username, password=password)
            # Attach session
            login(request, user)

            return redirect(reverse('show-user-profile', kwargs={
                                'username': username
                            }))

    return render(request, 'registration/register.html', {'form': form})
