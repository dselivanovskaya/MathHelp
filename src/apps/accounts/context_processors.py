from .apps import AccountsConfig as accounts_config


def accounts(request):
    return {
        'ACCOUNT_LOGIN_URL':    accounts_config.ACCOUNT_LOGIN_URL,
        'ACCOUNT_LOGOUT_URL':   accounts_config.ACCOUNT_LOGOUT_URL,
        'ACCOUNT_SETTINGS_URL': accounts_config.ACCOUNT_SETTINGS_URL,
        'ACCOUNT_CREATE_URL':   accounts_config.ACCOUNT_CREATE_URL,
        'ACCOUNT_DELETE_URL':   accounts_config.ACCOUNT_DELETE_URL,
        'ACCOUNT_PASSWORD_CHANGE_URL':   accounts_config.ACCOUNT_PASSWORD_CHANGE_URL,
        'ACCOUNT_USERNAME_CHANGE_URL':   accounts_config.ACCOUNT_USERNAME_CHANGE_URL,
    }
