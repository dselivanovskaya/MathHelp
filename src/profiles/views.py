from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.urls import reverse

from .forms import UpdateProfileForm
from .models import Profile
from .decorators import ownership_required


@login_required(redirect_field_name=None)
@ownership_required
def get_profile(request, username: str):
    ''' Returns user's profile page. '''
    context = {
        'user': User.objects.get(username=username),
    }
    return render(request, 'profiles/get-profile.html', context)


@login_required(redirect_field_name=None)
@ownership_required
def update_profile(request, username: str):

    if request.method == 'GET':
        form = UpdateProfileForm()

    elif request.method == 'POST':
        form = UpdateProfileForm(request.POST, request.FILES, instance=Profile.objects.get(user=request.user))
        if form.is_valid():
            form.save()
            return redirect(reverse('get-profile', args=[username]))

    return render(request, 'profiles/update-profile.html', {'form': form})


@login_required(redirect_field_name=None)
@ownership_required
def delete_profile(request, username: str):
    User.objects.get(username=username).delete()
    return redirect('/')
