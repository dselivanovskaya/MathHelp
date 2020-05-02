from django.shortcuts import redirect

from .apps import QuizConfig as quiz_config


def quiz_taken_required(view_func):

    def decorator(request, quiz_id, *args, **kwargs):

        if str(quiz_id) not in request.session['taken_quizzes']:
            return redirect(quiz_config.QUIZ_FORM_URL, quiz_id)

        return view_func(request, quiz_id, *args, **kwargs)

    return decorator


def quiz_not_taken_required(view_func):

    def decorator(request, quiz_id, *args, **kwargs):

        if str(quiz_id) in request.session['taken_quizzes']:
            return redirect(quiz_config.QUIZ_RESULT_URL, quiz_id)

        return view_func(request, quiz_id, *args, **kwargs)

    return decorator
