from django.urls import path

from .views import get_ticket_pdf, list_tickets

urlpatterns = [
    path('', list_tickets, name='tickets'),
    path('<str:filename>', get_ticket_pdf, name='ticket-pdf'),
]
