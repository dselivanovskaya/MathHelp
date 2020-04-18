from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.conf import settings
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views.generic.base import TemplateView
from django.views import View

from .apps import ProfilesConfig
from .forms import ProfileUpdateForm
from .models import Profile


@method_decorator(login_required(redirect_field_name=None), name='dispatch')
class ProfileView(TemplateView):

    url_name = 'profile'
    template_name = f'{ProfilesConfig.name}/profile.html'


@method_decorator(login_required(redirect_field_name=None), name='dispatch')
class ProfileRedirectView(View):
    ''' Redirects user to his profile. '''

    url_name = 'profile-redirect'

    def get(self, request):
        return redirect(ProfileView.url_name, request.user.username)


@method_decorator(login_required(redirect_field_name=None), name='dispatch')
class ProfileUpdateView(View):

    url_name = 'profile-update'
    form_class = ProfileUpdateForm
    template_name = f'{ProfilesConfig.name}/profile-update.html'

    def get(self, request, **kwargs):
        form = self.form_class(request.user, initial={
            'first_name': request.user.first_name,
            'last_name':  request.user.last_name,
            'email':      request.user.email,
            'username':   request.user.username,
            'gender':     request.user.profile.gender,
            'age':        request.user.profile.age,
        })
        return render(request, self.template_name, {'form': form})

    def post(self, request, **kwargs):
        form = self.form_class(
            request.user,
            request.POST,
            instance=Profile.objects.get(user=request.user)
        )
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated.')
            return redirect(self.url_name, request.user.username)
        return render(request, self.template_name, {'form': form})


@method_decorator(login_required(redirect_field_name=None), name='dispatch')
class ProfileDeleteView(View):

    url_name = 'profile-delete'

    def get(self, request, **kwargs):
        User.objects.get(username=request.user.username).delete()
        messages.success(request, 'Your profile has been deleted.')
        return redirect(settings.LOGIN_URL)
