from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
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
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']

            # Create user
            user = User.objects.create_user(username, email, password)
            # Login user
            user = authenticate(username=username, password=password)
            # Attach session
            login(request, user)

            return redirect(reverse('profile'))

    return render(request, 'registration/registration.html', {'form': form})
