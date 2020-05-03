from django.urls import path

from .apps import TicketsConfig
from .views import TicketDetailView, TicketListView, TicketPDFView


urlpatterns = [
    path(
        '',
        TicketListView.as_view(),
        name=TicketsConfig.TICKET_LIST_URL
    ),
    path(
        '<int:ticket_id>',
        TicketDetailView.as_view(),
        name=TicketsConfig.TICKET_DETAIL_URL
    ),
    path(
        '<str:ticket_filename>',
        TicketPDFView.as_view(),
        name=TicketsConfig.TICKET_PDF_URL
    ),
]
