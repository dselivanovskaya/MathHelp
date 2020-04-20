from django.urls import path


from .apps import AccountsConfig as app_conf
from .views import (
    AccountLoginView, AccountLogoutView,
    AccountSettingsView,
    AccountCreateView, AccountDeleteView
)

urlpatterns = [
    path('login',    AccountLoginView.as_view(),    name=app_conf.ACCOUNT_LOGIN_URL),
    path('logout',   AccountLogoutView.as_view(),   name=app_conf.ACCOUNT_LOGOUT_URL),
    path('settings', AccountSettingsView.as_view(), name=app_conf.ACCOUNT_SETTINGS_URL),
    path('create',   AccountCreateView.as_view(),   name=app_conf.ACCOUNT_CREATE_URL),
    path('delete',   AccountDeleteView.as_view(),   name=app_conf.ACCOUNT_DELETE_URL),
]
