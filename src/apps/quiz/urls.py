from django.urls import path

from .apps import QuizConfig as quiz_config
from .views import QuizTicketView


urlpatterns = [
    path(
        '<int:ticket_id>',
        QuizTicketView.as_view(),
        name=quiz_config.QUIZ_TICKET_URL
    ),
]
