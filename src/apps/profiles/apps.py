from django.apps import AppConfig


class ProfilesConfig(AppConfig):
    name = 'profiles'

    PROFILE_REDIRECT_URL = 'profile-redirect'
    PROFILE_DETAIL_URL = 'profile-detail'
    PROFILE_UPDATE_URL = 'profile-update'

    def ready(self):
        from . import signals
