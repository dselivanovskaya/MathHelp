from django.urls import path


from .apps import AccountsConfig as accounts_config
from .views import (
    AccountLoginView, AccountLogoutView,
    AccountSettingsView,
    AccountCreateView, AccountDeleteView,
    AccountPasswordChangeView,
    AccountUsernameChangeView,
)

urlpatterns = [
    path('login',    AccountLoginView.as_view(),    name=accounts_config.ACCOUNT_LOGIN_URL),
    path('logout',   AccountLogoutView.as_view(),   name=accounts_config.ACCOUNT_LOGOUT_URL),
    path('settings', AccountSettingsView.as_view(), name=accounts_config.ACCOUNT_SETTINGS_URL),
    path('create',   AccountCreateView.as_view(),   name=accounts_config.ACCOUNT_CREATE_URL),
    path('delete',   AccountDeleteView.as_view(),   name=accounts_config.ACCOUNT_DELETE_URL),
    path('password/change', AccountPasswordChangeView.as_view(),
        name=accounts_config.ACCOUNT_PASSWORD_CHANGE_URL),
    path('username/change', AccountUsernameChangeView.as_view(),
        name=accounts_config.ACCOUNT_USERNAME_CHANGE_URL),
]
