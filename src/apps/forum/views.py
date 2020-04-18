from django.contrib import messages
from django.shortcuts import redirect, render, reverse
from django.views import View

from tickets.models import Ticket

from .forms import CommentForm


class CommentPostView(View):

    def post(self, request, ticket_id):
        ticket = Ticket.objects.get(id=ticket_id)
        form = CommentForm(ticket, request.user, request.POST)
        if form.is_valid():
            comment = form.save()
            messages.success(request, 'Comment has been posted.')
        else:
            messages.error(request, 'Error')
        return redirect(reverse('ticket-detail', args=[ticket.id]))
