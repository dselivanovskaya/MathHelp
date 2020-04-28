from django.contrib import messages
from django.shortcuts import redirect, render, get_object_or_404
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.http import require_http_methods

from tickets.apps import TicketsConfig as tickets_config
from tickets.models import Ticket

from .forms import CommentForm
from .models import Comment


@method_decorator(require_http_methods(["POST"]), name='dispatch')
class CommentPostView(View):
    ''' Accepts a POST request to save a comment in database. '''

    form_class = CommentForm
    messages = {
        'error': 'Произошла ошибка во время оставления комментария.'
    }

    def post(self, request, ticket_id):
        ''' Validate and save a comment in database. '''
        ticket = get_object_or_404(Ticket, id=ticket_id)
        form = self.form_class(ticket, request.user, request.POST)
        if form.is_valid():
            form.save()
        else:
            messages.error(request, self.messages['error'])
        return redirect(tickets_config.TICKET_DETAIL_URL, ticket_id)


@method_decorator(require_http_methods(["GET"]), name='dispatch')
class CommentDeleteView(View):
    ''' Accepts a GET request to delete a particular comment. '''

    messages = {
        'error': 'У вас нет разрешения удалять этот комментарий.'
    }

    def get(self, request, comment_id):
        '''
            If user owns the comment - delete it, else report an error.
        '''
        comment = get_object_or_404(Comment, id=comment_id)
        if request.user == comment.user:
            comment.delete()
        else:
            messages.error(request, self.messages['error'])
        return redirect(tickets_config.TICKET_DETAIL_URL, comment.ticket.id)
