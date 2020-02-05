from django.shortcuts import redirect, render, reverse

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm


def login_request(request):
    """ Log in user. """
    if request.method == "POST":
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now looged in as {username}")
                return redirect(reverse("home"))
            else:
                messages.error(request, "Invalid username or password.")

    form = AuthenticationForm()
    return render(request, "registration/login.html", {"form": form})


def logout_request(request):
    """ Log out user. """
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect(reverse("home"))

