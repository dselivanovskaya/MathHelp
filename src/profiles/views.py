from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.urls import reverse

from .forms import ProfileUpdateForm
from .decorators import ownership_required


@login_required(redirect_field_name=None)
@ownership_required
def get_user_profile(request, username: str):
    ''' Returns user's profile page. '''
    context = {
        'user': User.objects.get(username=username),
    }
    return render(request, 'profiles/user-profile.html', context)


@login_required(redirect_field_name=None)
@ownership_required
def update_user_profile(request, username: str):

    if request.method == 'GET':
        form = ProfileUpdateForm()

    elif request.method == 'POST':
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
            return redirect(reverse('user-profile', args=[user.username]))
        else:
            ''' error '''

    return render(request, 'profiles/update-user-profile.html', {'form': form})


@login_required(redirect_field_name=None)
@ownership_required
def delete_user_profile(request, username: str):
    User.objects.get(username=username).delete()
    return redirect('/')
