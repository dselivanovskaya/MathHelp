from django.urls import path

from .views import TicketListView, TicketDetailView, TicketReadPDFView
from quiz.views import TicketQuizView

urlpatterns = [
    path('', TicketListView.as_view(), name='ticket-list'),
    path('/<int:id>', TicketDetailView.as_view(), name='ticket-detail'),
    path('/<int:id>/read', TicketReadPDFView.as_view(), name='ticket-read-pdf'),
    path('/<int:id>/quiz', TicketQuizView.as_view(), name='ticket-quiz'),
]
