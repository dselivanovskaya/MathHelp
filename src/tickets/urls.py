from django.urls import path

from .views import show_ticket_pdf, show_tickets

urlpatterns = [
    path('', show_tickets, name='show-tickets'),
    path('<slug:slug>', show_ticket_pdf, name='show-ticket-pdf'),
]
