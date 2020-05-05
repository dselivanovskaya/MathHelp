from django.urls import path

from .apps import QuizConfig
from .views import (
    QuizFormView, QuizResultView,
    QuizSaveView, QuizRestartView, QuizReportView,
)


urlpatterns = [
    path(
        '<int:quiz_id>',
        QuizFormView.as_view(),
        name=QuizConfig.QUIZ_FORM_URL,
    ),
    path(
        '<int:quiz_id>/result',
        QuizResultView.as_view(),
        name=QuizConfig.QUIZ_RESULT_URL,
    ),
    path(
        '<int:quiz_id>/result/save',
        QuizSaveView.as_view(),
        name=QuizConfig.QUIZ_SAVE_URL,
    ),
    path(
        '<int:quiz_id>/restart',
        QuizRestartView.as_view(),
        name=QuizConfig.QUIZ_RESTART_URL,
    ),
    path(
        '<int:quiz_id>/report',
        QuizReportView.as_view(),
        name=QuizConfig.QUIZ_REPORT_URL,
    ),
]
