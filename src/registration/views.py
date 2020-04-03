from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django import forms
from django.forms import ValidationError

from profiles.models import Profile

from .forms import UserRegistrationForm


def register(request):

    if request.method == 'POST':

        form = UserRegistrationForm(request.POST)
        if form.is_valid():

            username = form.cleaned_data['username']
            gender   = form.cleaned_data['gender']
            email    = form.cleaned_data['email']
            password = form.cleaned_data['password']

            # If user with that username or email doesn't exist
            if not (User.objects.filter(username=username).exists() or
                    User.objects.filter(email=email).exists()):

                # Create user
                user = User.objects.create_user(username, email, password)
                # Create profile
                Profile.objects.create(user=user, gender=gender)

                user = authenticate(username=username, password=password)
                login(request, user)

                return redirect(reverse('show-user-profile', kwargs={
                        'username': username
                        }))

            else: # user with 'username' or 'email' exists
                msg = "User with that 'username' or 'email' already exists:("
                messages.error(request, msg)
    else:
        form = UserRegistrationForm()

    return render(request, "registration/register.html", {"form": form})
