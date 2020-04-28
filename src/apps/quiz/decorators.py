from django.shortcuts import redirect

from .apps import QuizConfig as quiz_config


def quiz_taken_required(view_func):
    ''' Check if quiz_id is inside request.session['taken_quizzes']. '''
    def decorator(request, quiz_id, *args, **kwargs):

        if str(quiz_id) not in request.session['taken_quizzes']:
            return redirect(quiz_config.QUIZ_TICKET_URL, quiz_id)

        return view_func(request, quiz_id, *args, **kwargs)

    return decorator
