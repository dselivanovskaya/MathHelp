from django.urls import path

from .apps import ForumConfig as forum_config
from .views import CommentPostView, CommentDeleteView


urlpatterns = [
    path(
        'comment/post/<int:ticket_id>',
         CommentPostView.as_view(),
         name=forum_config.COMMENT_POST_URL,
    ),
    path(
        'comment/delete/<int:comment_id>',
        CommentDeleteView.as_view(),
        name=forum_config.COMMENT_DELETE_URL,
    ),
]
