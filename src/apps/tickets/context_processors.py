from .apps import TicketsConfig


def tickets(request):
    return {
        'TICKET_LIST_URL':     TicketsConfig.TICKET_LIST_URL,
    }
