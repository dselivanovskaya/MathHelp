import os

from django.http import FileResponse, Http404
from django.shortcuts import render

from .models import Ticket


def show_tickets(request):
    ''' List all tickets on the page. '''
    tickets = Ticket.objects.all()
    return render(request, "tickets/show.html", {"tickets": tickets})


def show_ticket_pdf(request, slug: str):
    ''' Return pdf-file for specific ticket. '''
    ticket = Ticket.objects.get(slug=slug)

    # Update user watched tickets in current session
    watched_tickets = request.session.get('watched_tickets', [])
    watched_tickets.append(ticket.name)
    request.session['watched_tickets'] = watched_tickets

    try:
        return FileResponse(open(os.path.abspath(os.path.join('tickets',
                            ticket.path)), 'rb'), content_type='application/pdf')
    except FileNotFoundError:
        raise Http404
