from django.apps import AppConfig


class QuizConfig(AppConfig):
    name = 'quiz'

    QUIZ_TICKET_URL = 'quiz-ticket'
    QUIZ_RESULT_URL = 'quiz-result'
    QUIZ_SAVE_URL = 'quiz-save'
    QUIZ_RESTART_URL = 'quiz-restart'
    QUIZ_REPORT_URL = 'quiz-report'
