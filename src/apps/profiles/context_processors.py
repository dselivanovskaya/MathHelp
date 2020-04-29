from .apps import ProfilesConfig


def profiles(request):
    return {
        'PROFILE_REDIRECT_URL': ProfilesConfig.PROFILE_DETAIL_URL,
        'PROFILE_DETAIL_URL':   ProfilesConfig.PROFILE_DETAIL_URL,
        'PROFILE_UPDATE_URL':   ProfilesConfig.PROFILE_UPDATE_URL,
    }
