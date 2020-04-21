from django.urls import path

from .apps import QuizzesConfig as quizzes_config
from .views import QuizTicketView


urlpatterns = [
    path(
        '<int:ticket_id>',
        QuizTicketView.as_view(),
        name=quizzes_config.QUIZ_TICKET_URL
    ),
]
