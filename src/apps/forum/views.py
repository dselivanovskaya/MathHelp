from django.contrib import messages

from django.shortcuts import redirect, get_object_or_404

from django.views import View

from tickets.apps import TicketsConfig
from tickets.models import Ticket

from .forms import CommentForm
from .models import Comment


class CommentCreateView(View):
    ''' Create a new Comment. '''

    form_class = CommentForm
    error_message = 'Произошла ошибка во время оставления комментария.'

    def post(self, request, ticket_id):
        ''' Validate and save a comment in database. '''
        ticket = get_object_or_404(Ticket, id=ticket_id)
        form = self.form_class(ticket, request.user, request.POST)
        if form.is_valid():
            form.save()
        else:
            messages.error(request, self.error_message)
        return redirect(TicketsConfig.TICKET_DETAIL_URL, ticket_id)


class CommentDeleteView(View):
    ''' Delete a particular Comment. '''

    error_message = 'У вас нет разрешения удалять этот комментарий.'

    def post(self, request, comment_id):
        '''
            If user owns the comment - delete it, else report an error.
        '''
        comment = get_object_or_404(Comment, id=comment_id)
        if request.user == comment.user:
            comment.delete()
        else:
            messages.error(self.error_message)
        return redirect(TicketsConfig.TICKET_DETAIL_URL, comment.ticket.id)
