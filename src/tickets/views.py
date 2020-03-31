from django.shortcuts import render
from django.http import HttpResponse, FileResponse, Http404
from .models import Ticket

import os

# Create your views here.

def show_tickets(request):
    tickets = Ticket.objects.all()
    return render(request, "tickets/show.html", {"tickets": tickets})


def show_ticket_pdf(request, slug: str):
    ticket = Ticket.objects.get(slug=slug)

    watched_tickets = request.session.get('watched_tickets', [])
    watched_tickets.append(ticket.name)
    request.session['watched_tickets'] = watched_tickets

    try:
        return FileResponse(open(os.path.abspath(os.path.join('tickets',
                                ticket.path)), 'rb'), content_type='application/pdf')
    except FileNotFoundError:
        raise Http404
