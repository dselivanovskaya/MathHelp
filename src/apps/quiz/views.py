from django.contrib import messages
from django.utils.decorators import method_decorator
from django.conf import settings
from django.shortcuts import redirect, render, get_object_or_404
from django.views import View
from django.views.decorators.http import require_http_methods
from django.core.exceptions import ObjectDoesNotExist

from tickets.apps import TicketsConfig as tickets_config

from .apps import QuizConfig as quiz_config
from .decorators import quiz_taken_required
from .forms import QuizForm
from .models import Quiz, Question, Answer, Result


QUIZ_ACTION_DECORATORS = [
    require_http_methods(["GET"]), quiz_taken_required,
]


class QuizTicketView(View):

    template_name = f'{quiz_config.name}/quiz-ticket.html'
    form_class = QuizForm

    def get(self, request, quiz_id):
        '''
            Render quiz form.

            If user has taken this quiz in the current session, redirect to
            that quiz result page.

            If user has not yet seen this quiz, update
            session['watched_quizzes'].
        '''
        if str(quiz_id) in request.session['taken_quizzes']:
            return redirect(quiz_config.QUIZ_RESULT_URL, quiz_id)

        quiz = get_object_or_404(Quiz, id=quiz_id)
        quiz.session_update(request, 'watched_quizzes')

        context = {
            'quiz': quiz,
            'form': self.form_class(quiz),
        }

        return render(request, self.template_name, context)

    def post(self, request, quiz_id):
        '''
            Calculate quiz result and store it in the session.

            If user has taken this quiz in the current session, redirect to
            that quiz result page.

            If form is valid, calculate total percentage of correct answers,
            store it in the current session alongside with quiz_id, quiz_name
            and saved flad.

            Redirect to quiz result page.
        '''
        if str(quiz_id) in request.session['taken_quizzes']:
            return redirect(quiz_config.QUIZ_RESULT_URL, quiz_id)

        quiz = get_object_or_404(Quiz, id=quiz_id)
        form = self.form_class(quiz, request.POST)

        if form.is_valid():
            request.session['taken_quizzes'].update({
                str(quiz_id): {
                    'name':    quiz.ticket.name,
                    'result':  form.cleaned_data['result'],
                    'answers': form.cleaned_data['answers'],
                    'saved':   False,
                }
            })
            return redirect(quiz_config.QUIZ_RESULT_URL, quiz_id)

        context = {
            'quiz': quiz,
            'form': form,
        }

        return render(request, self.template_name, context)


@method_decorator(QUIZ_ACTION_DECORATORS, name='dispatch')
class QuizResultView(View):

    template_name = f'{quiz_config.name}/quiz-result.html'

    def get(self, request, quiz_id):
        '''
            Display quiz result.

            If user has not yet taken the quiz, that he requests result for,
            redirect him to that quiz page, else return quiz result.

            If user has not yet saved the quiz result, allow to save it,
            else do not.
        '''
        quiz = get_object_or_404(Quiz, id=quiz_id)
        taken_quizzes = request.session['taken_quizzes']

        context = {
            'quiz':        quiz,
            'quiz_result': taken_quizzes[str(quiz_id)]['result'],
            'quiz_saved':  taken_quizzes[str(quiz_id)]['saved'],
        }

        return render(request, self.template_name, context)


@method_decorator(QUIZ_ACTION_DECORATORS, name='dispatch')
class QuizSaveView(View):

    success_message = 'Ваш результат был успешно сохранён.'

    def get(self, request, quiz_id):
        '''
            Save quiz result to the database.

            If user has not yet taken the quiz, that he requests to save
            result for, redirect him to that quiz page.

            If user does not have a Result entry for this quiz in the
            database, then create a new one.

            If user has a Result entry for this quiz in the database,
            then update it.

            Mark quiz as saved in the session.
        '''
        quiz = get_object_or_404(Quiz, id=quiz_id)
        result = request.session['taken_quizzes'][str(quiz_id)]['result']

        try:
            prev_result = Result.objects.get(quiz=quiz, user=request.user)
        except ObjectDoesNotExist:
            new_result = Result.objects.create(
                quiz=quiz, user=request.user, percent=result
            )
            new_result.save()
        else:
            prev_result.percent = result
            prev_result.save()
        finally:
            messages.success(request, self.success_message)
            request.session['taken_quizzes'][str(quiz_id)]['saved'] = True
            return redirect(settings.LOGIN_REDIRECT_URL)


@method_decorator(QUIZ_ACTION_DECORATORS, name='dispatch')
class QuizRestartView(View):

    success_message = 'Результат успешно сброшен.'
    error_message =  'Произошла ошибка во время сброса результата.',

    def get(self, request, quiz_id):
        ''' Delete 'quiz_id' from session['taken_quizzes']. '''
        try:
            del request.session['taken_quizzes'][str(quiz_id)]
        except:
            messages.error(request, self.error_message)
        else:
            messages.success(request, self.success_message)
        finally:
            return redirect(quiz_config.QUIZ_TICKET_URL, quiz_id)


@method_decorator(QUIZ_ACTION_DECORATORS, name='dispatch')
class QuizReportView(View):

    template_name = f'{quiz_config.name}/quiz-report.html'

    def get(self, request, quiz_id):
        '''  '''
        quiz = get_object_or_404(Quiz, id=quiz_id)
        taken_quiz_data = request.session['taken_quizzes'][str(quiz_id)]

        questions = Question.objects.filter(quiz=quiz)
        for question in questions:
            user_answer_id =  taken_quiz_data['answers'][str(question.id)]
            user_answer = Answer.objects.get(id=user_answer_id)
            question.user_answer = user_answer
            question.correct_answer = question.get_correct_answer()

        context = {
            'quiz': quiz,
            'taken_quiz_data': taken_quiz_data,
            'questions': questions,
        }

        return render(request, self.template_name, context)
