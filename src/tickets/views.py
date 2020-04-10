from django.http import FileResponse, Http404
from django.shortcuts import render, get_object_or_404
from django.views import View

from .models import Ticket


class TicketListView(View):

    template_name = 'tickets/ticket-list.html'

    def get(self, request):
        context = {'tickets': Ticket.objects.all()}
        return render(request, self.template_name, context)


class TicketDetailView(View):

    template_name = 'tickets/ticket-detail.html'

    def get(self, request, id):
        ticket = get_object_or_404(Ticket, id=id)
        return render(request, self.template_name, {'ticket': ticket})


class TicketReadPDFView(View):

    def get(self, request, id):
        ticket = get_object_or_404(Ticket, id=id)
        if ticket.name not in request.session['watched_tickets']:
            request.session['watched_tickets'].append(ticket.name)
        try:
            return FileResponse(open(ticket.get_absolute_path(), 'rb'))
        except FileNotFoundError:
            raise Http404
