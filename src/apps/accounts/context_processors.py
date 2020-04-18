from django.conf import settings


def url_names(request):
    return {
        'LOGIN_URL': settings.LOGIN_URL,
        'REGISTER_URL': settings.REGISTER_URL,
        'LOGOUT_URL': settings.LOGOUT_URL,
    }
