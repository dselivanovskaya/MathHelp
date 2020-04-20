from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic.base import TemplateView

from .apps import ProfilesConfig as profiles_config
from .forms import ProfileUpdateForm
from .models import Profile


@method_decorator(login_required(redirect_field_name=None), name='dispatch')
class ProfileRedirectView(View):
    ''' Redirects user to his profile. '''

    def get(self, request):
        return redirect(
            profiles_config.PROFILE_DETAIL_URL, request.user.username
        )


@method_decorator(login_required(redirect_field_name=None), name='dispatch')
class ProfileDetailView(TemplateView):

    template_name = f'{profiles_config.name}/profile-detail.html'


@method_decorator(login_required(redirect_field_name=None), name='dispatch')
class ProfileUpdateView(View):

    form_class = ProfileUpdateForm
    template_name = f'{profiles_config.name}/profile-update.html'

    messages = {
        'success': 'Профиль был успешно обновлен.'
    }

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
            messages.success(request, self.messages['success'])
            return redirect(
                profiles_config.PROFILE_UPDATE_URL, request.user.username
            )
        return render(request, self.template_name, {'form': form})
