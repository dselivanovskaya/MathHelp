from django.http import FileResponse
from django.shortcuts import get_object_or_404

from django.views import View
from django.views.generic import ListView
from django.views.generic.detail import DetailView

from forum.forms import CommentCreateForm

from .apps import TicketsConfig
from .models import Ticket


class TicketListView(ListView):
    ''' List all tickets. '''

    model = Ticket
    template_name = f'{TicketsConfig.name}/ticket-list.html'
    context_object_name = 'tickets'


class TicketDetailView(DetailView):
    ''' Show information about a particular ticket. '''

    model = Ticket
    template_name = f'{TicketsConfig.name}/ticket-detail.html'
    pk_url_kwarg = 'ticket_id'

    def get_context_data(self, **kwargs):
        ''' Return Comments and CommentForm. '''
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentCreateForm(self.get_object(), self.request.user)
        return context


class TicketPDFView(View):

    def get(self, request, ticket_filename):
        ticket = get_object_or_404(Ticket, filename=ticket_filename)

        if ticket.id not in request.session['read_tickets']:
            request.session['read_tickets'].append(ticket.id)

        return FileResponse(ticket.pdf)
