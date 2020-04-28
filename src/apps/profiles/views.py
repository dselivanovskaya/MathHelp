from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin

from django.urls import reverse, reverse_lazy

from django.views.generic import RedirectView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView

from .apps import ProfilesConfig
from .forms import ProfileUpdateForm
from .models import Profile


class ProfileRedirectView(RedirectView):
    ''' Redirect user to his profile. '''

    def get_redirect_url(self, *args, **kwargs):
        return reverse(
            ProfilesConfig.PROFILE_DETAIL_URL, args=[self.request.user.username]
        )


class ProfileDetailView(DetailView):
    ''' Display profile information and quiz results. '''

    template_name = f'{ProfilesConfig.name}/profile-detail.html'

    def get_object(self):
        return None

    def get_context_data(self, **kwargs):
        ''' Add quiz results to context. '''
        context = super().get_context_data(**kwargs)
        context['results'] = self.request.user.result_set.all()
        return context


class ProfileUpdateView(SuccessMessageMixin, UpdateView):

    model = Profile
    form_class = ProfileUpdateForm
    template_name = f'{ProfilesConfig.name}/profile-update.html'
    success_url = reverse_lazy(ProfilesConfig.PROFILE_REDIRECT_URL)
    success_message = 'Профиль был успешно обновлён.'

    def get_object(self):
        return self.request.user.profile
