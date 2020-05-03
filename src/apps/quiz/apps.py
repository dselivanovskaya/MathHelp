from django.apps import AppConfig


class QuizConfig(AppConfig):
    name = 'quiz'

    QUIZ_FORM_URL = 'quiz-form'
    QUIZ_RESULT_URL = 'quiz-result'
    QUIZ_SAVE_URL = 'quiz-save'
    QUIZ_RESTART_URL = 'quiz-restart'
    QUIZ_REPORT_URL = 'quiz-report'
