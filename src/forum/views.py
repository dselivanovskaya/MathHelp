from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.views import View
from .forms import CommentForm 

from tickets.models import Ticket

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
