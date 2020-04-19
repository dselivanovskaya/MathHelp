from django.contrib.auth.models import User
from django.db import models

from tickets.models import Ticket


class Comment(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField(max_length=2048)
    ticket = models.ForeignKey(Ticket, on_delete=models.SET_NULL, null = True)
