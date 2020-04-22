from django.http import FileResponse, Http404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404, render
from django.views import View
from django.views.generic import ListView

from forum.forms import CommentForm
from forum.models import Comment

from .apps import TicketsConfig as tickets_config
from .models import Ticket


@method_decorator(login_required(redirect_field_name=None), name='dispatch')
class TicketListView(ListView):

    model = Ticket
    template_name = f'{tickets_config.name}/ticket-list.html'


@method_decorator(login_required(redirect_field_name=None), name='dispatch')
class TicketDetailView(View):

    form_class = CommentForm
    template_name = f'{tickets_config.name}/ticket-detail.html'

    def get(self, request, ticket_id):
        ticket = get_object_or_404(Ticket, id=ticket_id)

        if ticket.name not in request.session['watched_tickets']:
            request.session['watched_tickets'].append(ticket.name)

        context = {
                'form':     self.form_class(ticket, request.user),
                'ticket':   ticket,
                'comments': Comment.objects.filter(ticket__id=ticket_id)
        }
        return render(request, self.template_name, context)


@method_decorator(login_required(redirect_field_name=None), name='dispatch')
class TicketReadPDFView(View):

    def get(self, request, ticket_filename):
        ticket = get_object_or_404(Ticket, filename=ticket_filename)

        if ticket.name not in request.session['read_tickets']:
            request.session['read_tickets'].append(ticket.name)

        try:
            return FileResponse(open(ticket.get_absolute_path(), 'rb'))
        except FileNotFoundError:
            raise Http404
