from django.shortcuts import redirect


def ownership_required(function):
    '''
        Redirects user home if he is trying to access profile he doesn't own.
    '''
    def decorator(request, username: str, *args, **kwargs):
        if request.user.username != username:
            return redirect('/')
        return function(request, username, *args, **kwargs)

    return decorator
