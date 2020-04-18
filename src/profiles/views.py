from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import redirect, render, reverse
from django.utils.decorators import method_decorator
from django.views import View

from .forms import EditProfileForm
from .models import Profile


@method_decorator(login_required(redirect_field_name=None), name='dispatch')
class ProfileView(View):

    template_name = 'profiles/profile.html'

    def get(self, request):
        return render(request, self.template_name, {})


@method_decorator(login_required(redirect_field_name=None), name='dispatch')
class EditProfileView(View):

    form_class = EditProfileForm
    template_name = 'profiles/edit-profile.html'

    def get(self, request):
        form = self.form_class(initial={
            'first_name': request.user.first_name,
            'last_name' : request.user.last_name,
            'gender'    : request.user.profile.gender,
            'age'       : request.user.profile.age,
        })
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST,
            instance=Profile.objects.get(user=request.user)
        )
        if form.is_valid():
            form.save()
            return redirect(reverse('profile'))
        return render(request, self.template_name, {'form': form})


@method_decorator(login_required(redirect_field_name=None), name='dispatch')
class DeleteProfileView(View):

    def get(self, request):
        User.objects.get(username=request.user.username).delete()
        return redirect('/')
