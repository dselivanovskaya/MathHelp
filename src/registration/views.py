from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import redirect, render, reverse

from authentication.decorators import anonymous_required

from .forms import SignUpForm


@anonymous_required
def sign_up(request):
    if request.method == 'GET':
        form = SignUpForm()

    elif request.method == 'POST':
        form = SignUpForm(request.POST)

        if form.is_valid():
            form.save()
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1']
            )
            login(request, user)
            return redirect(reverse('profile'))

    return render(request, 'registration/registration.html', {'form': form})


def get_username_status(request):
    username = request.GET.get('username', None)
    response_data = {}

    if User.objects.filter(username=username).exists():
        response_data['result'] = 'error'
    else:
        response_data['result'] = 'success'

    return JsonResponse(response_data)
