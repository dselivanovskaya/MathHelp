from .apps import ForumConfig


def forum(request):
    return {
        'COMMENT_CREATE_URL': ForumConfig.COMMENT_CREATE_URL,
        'COMMENT_DELETE_URL': ForumConfig.COMMENT_DELETE_URL,
    }
