from django.apps import AppConfig


class ForumConfig(AppConfig):
    name = 'forum'

    FORUM_COMMENT_CREATE_URL = 'forum-comment-create'
    FORUM_COMMENT_DELETE_URL = 'forum-comment-delete'
