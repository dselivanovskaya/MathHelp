from django import forms

from .models import Comment


class CommentCreateForm(forms.ModelForm):
    ''' User fills out this form to post a comment on forum. '''

    class Meta:
        model = Comment
        fields = ['body']

    def __init__(self, ticket, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.use_required_attribute = False
        self.ticket = ticket
        self.user = user

    def save(self):
        body = self.cleaned_data.get('body')
        comment = Comment.objects.create(
            ticket=self.ticket, user=self.user, body=body
        )
        comment.save()
        return comment
