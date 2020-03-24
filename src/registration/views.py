from django.shortcuts import render, redirect
from django.urls import reverse

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages

from django import forms
from django.forms import ValidationError

from django.contrib import messages

from .forms import UserRegistrationForm
from profiles.models import UserProfile

def register(request):

    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user_object = form.cleaned_data
            username = user_object["username"]
            gender = user_object["gender"]
            email    = user_object["email"]
            password = user_object["password"]

            if not (User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists()):
                user = User.objects.create_user(username, email, password)
                UserProfile.objects.create(user=user, gender=gender)
                user = authenticate(username=username, password=password)
                login(request, user)
                return redirect(reverse("show-user-profile", kwargs={"username":
                username}))
            else: # user with 'username' or 'email' exists
                msg = "User with that 'username' or 'email' already exists:("
                messages.error(request, msg)
    else:
        form = UserRegistrationForm()

    return render(request, "registration/register.html", {"form": form})