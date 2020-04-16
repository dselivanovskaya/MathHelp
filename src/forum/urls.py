from django.urls import path
from .views import CommentPostView

urlpatterns = [
    path('post/comment/<int:ticket_id>', CommentPostView.as_view(), name='comment-post'),
]