from django.urls import path

from .views import get_ticket_pdf, list_tickets, get_ticket

urlpatterns = [
    path('', list_tickets, name='tickets'),
    path('<int:id>/', get_ticket, name='ticket_info'),
    path('<int:id>/<str:filename>', get_ticket_pdf, name='ticket-pdf'),
]
