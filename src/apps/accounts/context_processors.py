from .apps import AccountsConfig as app_conf


def url_names(request):
    return {
        'ACCOUNT_LOGIN_URL':    app_conf.ACCOUNT_LOGIN_URL,
        'ACCOUNT_LOGOUT_URL':   app_conf.ACCOUNT_LOGOUT_URL,
        'ACCOUNT_SETTINGS_URL': app_conf.ACCOUNT_SETTINGS_URL,
        'ACCOUNT_CREATE_URL':   app_conf.ACCOUNT_CREATE_URL,
        'ACCOUNT_DELETE_URL':   app_conf.ACCOUNT_DELETE_URL,
    }
