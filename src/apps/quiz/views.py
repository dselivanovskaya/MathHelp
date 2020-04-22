from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.conf import settings
from django.shortcuts import redirect, render, get_object_or_404
from django.views import View

from  accounts.decorators import session_required
from tickets.apps import TicketsConfig as tickets_config

from .apps import QuizConfig as quiz_config
from .forms import QuizForm
from .models import Quiz, Result


@method_decorator(login_required(redirect_field_name=None), name='dispatch')
class QuizTicketView(View):

    template_name = f'{quiz_config.name}/quiz-ticket.html'
    form_class = QuizForm

    def get(self, request, quiz_id):
        '''
            Update session['watched_quizzes'] and return a QuizForm.
        '''
        quiz = get_object_or_404(Quiz, id=quiz_id)
        quiz.session_update(request, 'watched_quizzes')

        if request.session['taken_quizzes'].get(str(quiz_id)):
            return redirect(quiz_config.QUIZ_RESULT_URL, quiz_id)

        context = {
            'quiz': quiz,
            'form': self.form_class(quiz),
        }

        return render(request, self.template_name, context)

    def post(self, request, quiz_id):
        '''
            Validate QuizForm and calculate result.
            If it is valid, create a session['taken_quiz'] entry, store
            result in there and redirect to QuizResultView.
        '''
        quiz = get_object_or_404(Quiz, id=quiz_id)
        form = self.form_class(quiz, request.POST)

        if request.session['taken_quizzes'].get(str(quiz_id)):
            return redirect(quiz_config.QUIZ_RESULT_URL, quiz_id)

        if form.is_valid():
            request.session['taken_quizzes'].update({
                str(quiz_id): {
                    'name':    quiz.ticket.name,
                    'percent': form.cleaned_data['percent'],
                }
            })
            return redirect(quiz_config.QUIZ_RESULT_URL, quiz_id)

        context = {
            'quiz': quiz,
            'form': form,
        }

        return render(request, self.template_name, context)


@method_decorator(login_required(redirect_field_name=None), name='dispatch')
class QuizResultView(View):

    template_name = f'{quiz_config.name}/quiz-result.html'

    def get(self, request, quiz_id):
        '''

        '''
        quiz = get_object_or_404(Quiz, id=quiz_id)

        # If user didn't take a quiz on this ticket
        if not request.session['taken_quizzes'].get(str(quiz_id)):
            return redirect(quiz_config.QUIZ_TICKET_URL, quiz_id)

        context = {
            'quiz': quiz,
            'percent': request.session['taken_quizzes'][str(quiz_id)]['percent'],
        }

        return render(request, self.template_name, context)


@method_decorator(login_required(redirect_field_name=None), name='dispatch')
class QuizSaveView(View):

    messages = {
        'success-update': 'Ваш результат был успешно обновлён.',
        'success-save':   'Ваш результат был успешно сохранён.',
    }

    def get(self, request, quiz_id):
        '''
            Save session['taken_quiz']['percent'] in database.
        '''
        quiz = get_object_or_404(Quiz, id=quiz_id)

        # If user didn't take a quiz on this ticket
        if not request.session['taken_quizzes'].get(str(quiz_id)):
            return redirect(quiz_config.QUIZ_TICKET_URL, quiz_id)

        percent = request.session['taken_quizzes'][str(quiz_id)]['percent']

        # Check if user already has a saved record for this quiz.
        user_results = Result.objects.filter(quiz=quiz, user=request.user)

        if user_results:
            # If he does, we update the result.
            prev_result = user_results.first()
            prev_result.percent = percent
            prev_result.save()
            messages.success(request, self.messages['success-update'])
        else:
            # If he doesn't, we create a new entry.
            new_result = Result.objects.create(
                quiz=quiz, user=request.user, percent=percent
            )
            new_result.save()
            messages.success(request, self.messages['success-save'])

        # ?? remove this quiz result from session??

        return redirect(settings.PROFILE_REDIRECT_URL)
