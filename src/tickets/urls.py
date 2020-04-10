from django.urls import path

from .views import TicketListView, TicketDetailView, TicketReadPDFView

urlpatterns = [
    path('', TicketListView.as_view(), name='ticket-list'),
    path('/<int:id>', TicketDetailView.as_view(), name='ticket-detail'),
    path('/<int:id>/read', TicketReadPDFView.as_view(), name='ticket-read-pdf'),
]
