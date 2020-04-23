from django.urls import path

from .apps import QuizConfig as quiz_config
from .views import QuizTicketView, QuizResultView, QuizSaveView, QuizRestartView


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
    ),
    path(
        '<int:quiz_id>/result/save',
        QuizSaveView.as_view(),
        name=quiz_config.QUIZ_SAVE_URL,
    ),
    path(
        '<int:quiz_id>/restart',
        QuizRestartView.as_view(),
        name=quiz_config.QUIZ_RESTART_URL,
    ),
]
