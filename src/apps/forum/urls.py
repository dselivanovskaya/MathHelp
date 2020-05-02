from django.urls import path

from .apps import ForumConfig
from .views import CommentCreateView, CommentDeleteView


urlpatterns = [
    path(
        'comment/create/<int:ticket_id>',
         CommentCreateView.as_view(),
         name=ForumConfig.FORUM_COMMENT_CREATE_URL,
    ),
    path(
        'comment/delete/<int:comment_id>',
        CommentDeleteView.as_view(),
        name=ForumConfig.FORUM_COMMENT_DELETE_URL,
    ),
]
