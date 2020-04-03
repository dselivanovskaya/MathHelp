from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django import forms
from django.forms import ValidationError

from profiles.models import Profile

from .forms import UserRegistrationForm
from .constants import USERNAME_NOT_AVAILABLE_ERROR_MESSAGE


def register(request):

    if request.method == 'POST':

        form = UserRegistrationForm(request.POST)
        if form.is_valid():

            username = form.cleaned_data['username']
            email    = form.cleaned_data['email']
            password = form.cleaned_data['password']

            # If user with that username or email doesn't exist
            if not (User.objects.filter(username=username).exists() or
                    User.objects.filter(email=email).exists()):

                # Create user
                user = User.objects.create_user(username, email, password)
                # Login user
                user = authenticate(username=username, password=password)
                # Attach session
                login(request, user)

                return redirect(reverse('show-user-profile', kwargs={
                                    'username': username
                                }))
            else:
                messages.error(request, USERNAME_NOT_AVAILABLE_ERROR_MESSAGE)
    else:
        form = UserRegistrationForm()

    return render(request, "registration/register.html", {"form": form})
