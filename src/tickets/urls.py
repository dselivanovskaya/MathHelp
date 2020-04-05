from django.urls import path

from .views import list_tickets, get_ticket_pdf

urlpatterns = [
    path('', list_tickets, name='tickets'),
    path('<slug:slug>', get_ticket_pdf, name='ticket-pdf'),
]
