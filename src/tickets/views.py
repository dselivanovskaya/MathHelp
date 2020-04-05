from django.http import FileResponse, Http404
from django.shortcuts import render

from .models import Ticket


def list_tickets(request):
    ''' Retusn a list of all tickets. '''
    return render(
        request, 'tickets/tickets.html', {'tickets': Ticket.objects.all()}
    )


def get_ticket_pdf(request, slug: str):
    ''' Return a ticket in pdf format. '''
    ticket = Ticket.objects.get(slug=slug)

    # Update user watched tickets in current session
    watched_tickets = request.session.get('watched_tickets', [])
    watched_tickets.append(ticket.name)
    request.session['watched_tickets'] = watched_tickets

    try:
        return FileResponse(open(ticket.get_absolute_path(), 'rb'))
    except FileNotFoundError:
        raise Http404
