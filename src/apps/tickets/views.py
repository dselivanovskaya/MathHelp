from django.http import FileResponse, Http404
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404, render
from django.views import View
from django.views.generic import ListView

from forum.forms import CommentForm
from forum.models import Comment

from .apps import TicketsConfig as tickets_config
from .models import Ticket


class TicketListView(ListView):

    model = Ticket
    template_name = f'{tickets_config.name}/ticket-list.html'


class TicketDetailView(View):

    form_class = CommentForm
    template_name = f'{tickets_config.name}/ticket-detail.html'

    def get(self, request, ticket_id):
        ticket = get_object_or_404(Ticket, id=ticket_id)
        ticket.session_update(request, 'watched_tickets')

        context = {
                'form':     self.form_class(ticket, request.user),
                'ticket':   ticket,
                'comments': Comment.objects.filter(ticket__id=ticket_id)
        }
        return render(request, self.template_name, context)


class TicketReadPDFView(View):

    def get(self, request, ticket_filename):
        ticket = get_object_or_404(Ticket, filename=ticket_filename)
        ticket.session_update(request, 'read_tickets')

        try:
            return FileResponse(open(ticket.get_absolute_path(), 'rb'))
        except FileNotFoundError:
            raise Http404
