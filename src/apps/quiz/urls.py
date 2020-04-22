from django.urls import path

from .apps import QuizConfig as quiz_config
from .views import QuizTicketView, QuizResultView


urlpatterns = [
    path(
        '<int:quiz_id>',
        QuizTicketView.as_view(),
        name=quiz_config.QUIZ_TICKET_URL,
    ),
    path(
        '<int:quiz_id>/result',
        QuizResultView.as_view(),
        name=quiz_config.QUIZ_RESULT_URL,
    )
]
