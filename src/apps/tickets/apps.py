from django.apps import AppConfig


class TicketsConfig(AppConfig):
    name = 'tickets'

    TICKET_LIST_URL = 'ticket-list'
    TICKET_DETAIL_URL = 'ticket-detail'
    TICKET_PDF_URL = 'ticket-pdf'
