from .apps import AccountsConfig


def accounts(request):
    return {
        'ACCOUNT_LOGIN_URL':           AccountsConfig.ACCOUNT_LOGIN_URL,
        'ACCOUNT_LOGOUT_URL':          AccountsConfig.ACCOUNT_LOGOUT_URL,
        'ACCOUNT_SETTINGS_URL':        AccountsConfig.ACCOUNT_SETTINGS_URL,
        'ACCOUNT_CREATE_URL':          AccountsConfig.ACCOUNT_CREATE_URL,
        'ACCOUNT_DELETE_URL':          AccountsConfig.ACCOUNT_DELETE_URL,
        'ACCOUNT_PASSWORD_CHANGE_URL': AccountsConfig.ACCOUNT_PASSWORD_CHANGE_URL,
        'ACCOUNT_USERNAME_UPDATE_URL': AccountsConfig.ACCOUNT_USERNAME_UPDATE_URL,
        'ACCOUNT_EMAIL_UPDATE_URL':    AccountsConfig.ACCOUNT_EMAIL_UPDATE_URL,
    }
