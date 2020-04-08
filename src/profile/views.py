from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.urls import reverse

from .forms import UpdateProfileForm
from .models import Profile


@login_required(redirect_field_name=None)
def get_profile(request):
    ''' Returns user's profile page. '''
    context = {
        'user': User.objects.get(username=request.user.username),
    }
    return render(request, 'profile/profile.html', context)


@login_required(redirect_field_name=None)
def update_profile(request):

    if request.method == 'GET':
        form = UpdateProfileForm()

    elif request.method == 'POST':
        form = UpdateProfileForm(request.POST, request.FILES, instance=Profile.objects.get(user=request.user))

        if form.is_valid():
            form.save()
            return redirect(reverse('get-profile'))

    return render(request, 'profile/update-profile.html', {'form': form})


@login_required(redirect_field_name=None)
def delete_profile(request):
    User.objects.get(username=request.user.username).delete()
    return redirect('/')
