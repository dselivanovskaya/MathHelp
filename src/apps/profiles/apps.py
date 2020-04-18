from django.apps import AppConfig


class ProfilesConfig(AppConfig):
    name = 'profiles'

    PROFILE_URL = 'profile'
    PROFILE_UPDATE_URL = 'profile-update'
    PROFILE_DELETE_URL = 'profile-delete'

    def ready(self):
        from . import signals
