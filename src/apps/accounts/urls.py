from django.urls import path

from .apps import AccountsConfig
from .views import (
    AccountLoginView, AccountLogoutView, AccountCreateView, AccountDeleteView,
    AccountPasswordChangeView, AccountUsernameUpdateView, AccountEmailUpdateView,
)


urlpatterns = [
    path(
        'login',
         AccountLoginView.as_view(),
         name=AccountsConfig.ACCOUNT_LOGIN_URL
    ),
    path(
        'logout',
        AccountLogoutView.as_view(),
        name=AccountsConfig.ACCOUNT_LOGOUT_URL
    ),
    path(
        'create',
        AccountCreateView.as_view(),
        name=AccountsConfig.ACCOUNT_CREATE_URL
    ),
    path(
        'delete',
        AccountDeleteView.as_view(),
        name=AccountsConfig.ACCOUNT_DELETE_URL
    ),
    path(
        'password/change',
        AccountPasswordChangeView.as_view(),
        name=AccountsConfig.ACCOUNT_PASSWORD_CHANGE_URL
    ),
    path(
        'username/update',
        AccountUsernameUpdateView.as_view(),
        name=AccountsConfig.ACCOUNT_USERNAME_UPDATE_URL
    ),
    path(
        'email/update',
        AccountEmailUpdateView.as_view(),
        name=AccountsConfig.ACCOUNT_EMAIL_UPDATE_URL
    ),
]
