from django.http import FileResponse, Http404
from django.shortcuts import render

from .models import Ticket


def list_tickets(request):
    ''' Retusn a list of all tickets. '''
    return render(
        request, 'tickets/tickets.html', {'tickets': Ticket.objects.all()}
    )


def get_ticket_pdf(request, id, filename: str):
    ''' Return a ticket in pdf format. '''
    ticket = Ticket.objects.get(filename=filename)
    if ticket.name not in request.session['watched_tickets']:
        request.session['watched_tickets'].append(ticket.name)
    print(ticket.get_absolute_path())
    try:
        return FileResponse(open(ticket.get_absolute_path(), 'rb'))
    except FileNotFoundError:
        raise Http404

def get_ticket(request, id):
    return render(
        request, 'tickets/ticket.html', {'ticket': Ticket.objects.get(id = id)}
    )