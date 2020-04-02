from django.shortcuts import render

from django.contrib.auth.models import User


def show_user_profile(request, username):
    user = User.objects.get(username=username)

    # Remove duplicates from current session watched tickets
    watched_tickets = request.session.get('watched_tickets', [])
    user.watched_tickets = set(watched_tickets)

    return render(request, "profiles/profile.html", {"user": user})

