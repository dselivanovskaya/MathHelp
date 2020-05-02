from .apps import ForumConfig


def forum(request):
    return {
        'FORUM_COMMENT_CREATE_URL': ForumConfig.FORUM_COMMENT_CREATE_URL,
        'FORUM_COMMENT_DELETE_URL': ForumConfig.FORUM_COMMENT_DELETE_URL,
    }
