from django.apps import AppConfig


class ForumConfig(AppConfig):
    name = 'forum'

    COMMENT_CREATE_URL = 'comment-create'
    COMMENT_DELETE_URL = 'comment-delete'
