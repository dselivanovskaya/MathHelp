from django.apps import AppConfig


class ForumConfig(AppConfig):
    name = 'forum'

    COMMENT_POST_URL = 'comment-post'
    COMMENT_DELETE_URL = 'comment-delete'
