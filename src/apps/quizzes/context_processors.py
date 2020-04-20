from .apps import QuizzesConfig as quizzes_config


def quizzes(request):
    return {
        'QUIZ_TICKET_URL': quizzes_config.QUIZ_TICKET_URL,
    }
