from django.apps import AppConfig


class AccountsConfig(AppConfig):
    name = 'accounts'

    ACCOUNT_LOGIN_URL = 'account-login'
    ACCOUNT_LOGOUT_URL = 'account-logout'
    ACCOUNT_SETTINGS_URL = 'account-settings'
    ACCOUNT_CREATE_URL = 'account-create'
    ACCOUNT_DELETE_URL = 'account-delete'
    ACCOUNT_PASSWORD_CHANGE_URL = 'account-password-change'
    ACCOUNT_USERNAME_UPDATE_URL = 'account-username-update'
    ACCOUNT_EMAIL_UPDATE_URL = 'account-email-update'

    def ready(self):
        from . import signals
