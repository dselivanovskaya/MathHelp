from django.contrib.auth import get_user_model
from django.db import models

from tickets.models import Ticket


class Comment(models.Model):
    '''
        Represents a single comment on forum.
        Every comment is bound to a particular TICKET and USER.
    '''
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    body = models.TextField(max_length=2048)

    def __str__(self):
        return (
            f"{str(self.user)}: {str(self.ticket)} "
            f"[ {self.date.strftime('%Y-%m-%d %H:%M:%S')} ]"
        )
