from django import forms
from django.forms import ModelForm

from .models import Comment


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)

    def __init__(self, ticket, user, *args, **kwargs):
        self.ticket = ticket
        self.user = user
        super().__init__(*args, **kwargs)

    def save(self):
        body = self.cleaned_data.get('body')
        comment = Comment.objects.create(creator=self.user, body=body, ticket=self.ticket)
        comment.save()
        return comment
