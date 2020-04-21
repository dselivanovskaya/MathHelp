from django.urls import path

from .apps import TicketsConfig as tickets_config
from .views import TicketDetailView, TicketListView, TicketReadPDFView


urlpatterns = [
    path(
        'list',
        TicketListView.as_view(),
        name=tickets_config.TICKET_LIST_URL
    ),
    path(
        '<int:ticket_id>',
        TicketDetailView.as_view(),
        name=tickets_config.TICKET_DETAIL_URL
    ),
    path(
        '<str:ticket_filename>',
        TicketReadPDFView.as_view(),
        name=tickets_config.TICKET_READ_PDF_URL
    ),
]
