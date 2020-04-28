from .apps import ForumConfig as forum_config


def forum(request):
    return {
        'COMMENT_POST_URL':   forum_config.COMMENT_POST_URL,
        'COMMENT_DELETE_URL': forum_config.COMMENT_DELETE_URL,
    }
