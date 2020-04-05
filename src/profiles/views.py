from django.shortcuts import render, redirect
from django.urls import reverse

from django.contrib.auth.models import User

from .forms import ProfileUpdateForm


def show_user_profile(request, username):
    if request.user.username != username:
        return redirect(reverse('home'))

    user = User.objects.get(username=username)
    # Remove duplicates from current session watched tickets
    watched_tickets = request.session.get('watched_tickets', [])
    user.watched_tickets = set(watched_tickets)

    return render(request, "profiles/user-profile.html", {"user": user})


def delete_user_profile(request, username):
    if request.user.username == username:
        User.objects.get(username=username).delete()
    return redirect(reverse('home'))


def update_user_profile(request, username):
    if request.user.username != username:
        return redirect(reverse('home'))

    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST)
        if form.is_valid():
            new_username = form.cleaned_data['username']
            new_email    = form.cleaned_data['email']
            new_password = form.cleaned_data['password']

            user = User.objects.get(username=username)

            if new_username:
                if not User.objects.filter(username=new_username).exists():
                    user.username = new_username
            if new_email:
                if not User.objects.filter(email=new_email).exists():
                    user.email = new_email
            if new_password:
                user.password = new_password
            user.save()
            return redirect(reverse("show-user-profile", kwargs={"username": user.username}))
        else:
            ''' error '''

    form = ProfileUpdateForm()
    return render(request, 'profiles/update.html', {'form': form})

