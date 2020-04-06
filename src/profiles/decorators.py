from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.shortcuts import redirect, reverse


def user_owns_profile(function):
    '''
        Redirects user home if he is trying to access profile he doesn't own.
    '''
    def decorator(request, username: str, *args, **kwargs):
        if request.user.username != username:
            return redirect('/')
        return function(request, username, *args, **kwargs)

    return decorator
