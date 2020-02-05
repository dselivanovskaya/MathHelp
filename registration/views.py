from django.shortcuts import render, redirect
from django.urls import reverse

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages

from django import forms

from .forms import UserRegistrationForm


def register(request):

    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user_object = form.cleaned_data
            username = user_object["username"]
            email    = user_object["email"]
            password = user_object["password"]
            if not (User.objects.filter(username=username).exists() or
                User.objects.filter(email=email).exists()):
                User.objects.create_user(username, email, password)
                user = authenticate(username=username, password=password)
                login(request, user)
                return redirect(reverse("home"))
            else:
                error_msg = "A User with that username or email alreafy exists!"
                return render(request, "registration/register_error.html",
                {"error_msg": error_msg})

    form = UserRegistrationForm()
    return render(request, "registration/register.html", {"form": form})

