from django.apps import AppConfig


class QuizConfig(AppConfig):
    name = 'quiz'

    QUIZ_TICKET_URL = 'quiz-ticket'
    QUIZ_RESULT_URL = 'quiz-result'
    QUIZ_SAVE_URL = 'quiz-save'
