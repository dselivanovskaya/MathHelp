from .apps import ProfilesConfig


def url_names(request):
    return {
        'PROFILE_URL':        ProfilesConfig.PROFILE_URL,
        'PROFILE_UPDATE_URL': ProfilesConfig.PROFILE_UPDATE_URL,
        'PROFILE_DELETE_URL': ProfilesConfig.PROFILE_DELETE_URL,
    }
