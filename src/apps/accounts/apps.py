from django.apps import AppConfig


class AccountsConfig(AppConfig):
    name = 'accounts'

    ACCOUNT_LOGIN_URL = 'account-login'
    ACCOUNT_LOGOUT_URL = 'account-logout'
    ACCOUNT_SETTINGS_URL = 'account-settings'
    ACCOUNT_CREATE_URL = 'account-create'
    ACCOUNT_DELETE_URL = 'account-delete'
    ACCOUNT_PASSWORD_CHANGE_URL = 'account-password-change'
    ACCOUNT_USERNAME_CHANGE_URL = 'account-username-change'

    def ready(self):
        from . import signals
