from django.contrib import messages
from django.shortcuts import redirect, render, reverse

from django.views import View
from django.views.generic import RedirectView
from django.views.generic.detail import DetailView

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
        ''' Overriden DetailView method. '''
        return None

    def get_context_data(self, **kwargs):
        ''' Add quiz results to context. '''
        context = super().get_context_data(**kwargs)
        context['results'] = self.request.user.result_set.all()
        return context


# TODO two models in one form, cant detect proper changes, always says that
# mode lhas been updated.
class ProfileUpdateView(View):

    form_class = ProfileUpdateForm
    template_name = f'{ProfilesConfig.name}/profile-update.html'

    messages = {
        'success': 'Профиль был успешно обновлён.'
    }

    def get(self, request, **kwargs):
        ''' Populate form with user profile data. '''
        form = self.form_class(request.user, initial={
            'first_name': request.user.first_name,
            'last_name':  request.user.last_name,
            'photo':      request.user.profile.photo,
            'gender':     request.user.profile.gender,
            'age':        request.user.profile.age,
        })
        return render(request, self.template_name, {'form': form})

    def post(self, request, **kwargs):
        form = self.form_class(
            request.user, request.POST, request.FILES,
            instance=request.user.profile,
        )
        if form.is_valid():
            form.save()
            messages.success(request, self.messages['success'])
            return redirect(
                ProfilesConfig.PROFILE_UPDATE_URL, request.user.username
            )
        return render(request, self.template_name, {'form': form})
