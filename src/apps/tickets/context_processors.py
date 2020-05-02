from .apps import TicketsConfig


def tickets(request):
    return {
        'TICKET_LIST_URL':     TicketsConfig.TICKET_LIST_URL,
        'TICKET_DETAIL_URL':   TicketsConfig.TICKET_DETAIL_URL,
    }
