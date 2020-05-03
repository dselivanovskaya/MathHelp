from .apps import QuizConfig


def quiz(request):
    return {
        'QUIZ_FORM_URL':    QuizConfig.QUIZ_FORM_URL,
        'QUIZ_RESULT_URL':  QuizConfig.QUIZ_RESULT_URL,
        'QUIZ_SAVE_URL':    QuizConfig.QUIZ_SAVE_URL,
        'QUIZ_RESTART_URL': QuizConfig.QUIZ_RESTART_URL,
        'QUIZ_REPORT_URL':  QuizConfig.QUIZ_REPORT_URL,
    }
