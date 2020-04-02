from django.shortcuts import render, redirect
from django.urls import reverse

from django.contrib.auth.models import User


def show_user_profile(request, username):
    if request.user.username != username:
        return redirect(reverse('home'))

    user = User.objects.get(username=username)
    # Remove duplicates from current session watched tickets
    watched_tickets = request.session.get('watched_tickets', [])
    user.watched_tickets = set(watched_tickets)

    return render(request, "profiles/profile.html", {"user": user})


def delete_user_profile(request, username):
    if request.user.username == username:
        User.objects.get(username=username).delete()
    return redirect(reverse('home'))