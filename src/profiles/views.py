from django.shortcuts import render

from django.contrib.auth.models import User

# Create your views here.

def show_user_profile(request, username):
    user = User.objects.get(username=username)

    watched_tickets = request.session.get('watched_tickets', [])
    user.watched_tickets = watched_tickets
    return render(request, "profiles/profile.html", {"user": user})

