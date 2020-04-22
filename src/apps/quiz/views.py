from django.contrib import messages
from django.conf import settings
from django.shortcuts import redirect, render, get_object_or_404
from django.views import View

from .apps import QuizConfig as quiz_config
from .forms import QuizForm
from .models import Quiz, Result


class QuizTicketView(View):

    template_name = f'{quiz_config.name}/quiz-ticket.html'
    form_class = QuizForm

    def get(self, request, quiz_id):
        quiz = get_object_or_404(Quiz, id=quiz_id)

        if quiz.ticket.name not in request.session['watched_quizzes']:
            request.session['watched_quizzes'].append(quiz.ticket.name)

        context = {
            'quiz': quiz,
            'form': self.form_class(quiz),
        }

        return render(request, self.template_name, context)

    def post(self, request, quiz_id):
        quiz = get_object_or_404(Quiz, id=quiz_id)
        form = self.form_class(quiz, request.POST)

        if form.is_valid():
            result = form.cleaned_data['result']
            request.session['taken_quiz_id'] = quiz_id
            request.session['taken_quiz_result'] = result
            return redirect(quiz_config.QUIZ_RESULT_URL, quiz_id)

        context = {
            'quiz': quiz,
            'form': form,
        }
        return render(request, self.template_name, context)


# TODO: Add a decorator that restricts access for those who didn't take this test.
class QuizResultView(View):

    template_name = f'{quiz_config.name}/quiz-result.html'

    messages = {
        'success-update': 'Ваш результат был успешно обновлён.',
        'success-save':   'Ваш результат был успешно сохранён.',
    }

    def get(self, request, quiz_id):
        # If a client tries to access a quiz result he didn't take.
        if quiz_id != request.session.get('taken_quiz_id'):
            # Redirect him to this quiz page.
            return redirect(quiz_config.QUIZ_TICKET_URL, quiz_id)

        quiz = get_object_or_404(Quiz, id=quiz_id)

        if quiz.ticket.name not in request.session['taken_quizzes']:
            request.session['taken_quizzes'].append(quiz.ticket.name)

        context = {
            'quiz': quiz,
            'result': request.session.get('taken_quiz_result'),
        }
        return render(request, self.template_name, context)

    def post(self, request, quiz_id):
        quiz = get_object_or_404(Quiz, id=quiz_id)
        quiz_result = request.session.get('taken_quiz_result')

        # Check if user already has a saved record for this quiz.
        user_results = Result.objects.filter(quiz=quiz, user=request.user)

        if user_results:
            # If he does, we update the result.
            last_result = user_results.first()
            last_result.percent = quiz_result
            last_result.save()
            messages.success(request, self.messages['success-update'])
        else:
            # If he doesn't, we create a new entry.
            new_result = Result.objects.create(
                quiz=quiz, user=request.user, percent=quiz_result
            )
            new_result.save()
            messages.success(request, self.messages['success-save'])

        # Remove quiz result from the session
        del request.session['taken_quiz_id']
        del request.session['taken_quiz_result']

        return redirect(settings.PROFILE_REDIRECT_URL)
