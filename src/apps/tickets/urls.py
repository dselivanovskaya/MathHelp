from django.urls import path

from .apps import TicketsConfig
from .views import TicketDetailView, TicketListView, TicketReadPDFView


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
        TicketReadPDFView.as_view(),
        name=TicketsConfig.TICKET_READ_PDF_URL
    ),
]
