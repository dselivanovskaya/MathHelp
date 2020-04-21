from .apps import TicketsConfig as tickets_config


def tickets(request):
    return {
        'TICKET_LIST_URL':     tickets_config.TICKET_LIST_URL,
        'TICKET_DETAIL_URL':   tickets_config.TICKET_DETAIL_URL,
        'TICKET_READ_PDF_URL': tickets_config.TICKET_READ_PDF_URL,
    }
