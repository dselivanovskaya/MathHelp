from django.conf import settings
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse
from django.utils.decorators import method_decorator

from django.views import View
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView

from tickets.apps import TicketsConfig

from .apps import QuizConfig
from .decorators import quiz_taken_required, quiz_not_taken_required
from .forms import QuizForm
from .models import Quiz, Question, Answer, Result


@method_decorator(quiz_not_taken_required, name='dispatch')
class QuizFormView(FormView):

    form_class = QuizForm
    template_name = f'{QuizConfig.name}/quiz-form.html'

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super().get_form_kwargs(*args, **kwargs)
        self.quiz = Quiz.objects.get(id=self.kwargs.get('quiz_id'))
        kwargs['quiz'] = self.quiz
        return kwargs

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['quiz'] = self.quiz
        return context

    def form_valid(self, form):
        self.request.session.get('taken_quizzes').update({
            self.quiz.id: {
                'name':    self.quiz.ticket.name,
                'result':  form.cleaned_data['result'],
                'answers': form.cleaned_data['answers'],
                'saved':   False,
            }
        })
        return super().form_valid(form)

    def get_success_url(self):
        return reverse(QuizConfig.QUIZ_RESULT_URL, args=[self.quiz.id])


@method_decorator(quiz_taken_required, name='dispatch')
class QuizResultView(TemplateView):

    template_name = f'{QuizConfig.name}/quiz-result.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        taken_quizzes = self.request.session.get('taken_quizzes')
        quiz = get_object_or_404(Quiz, id=self.kwargs.get('quiz_id'))
        quiz.result = taken_quizzes.get(str(quiz.id)).get('result')
        quiz.saved = taken_quizzes.get(str(quiz.id)).get('saved')
        context['quiz'] = quiz
        return context


@method_decorator(quiz_taken_required, name='dispatch')
class QuizSaveView(View):

    success_message = 'Ваш результат был успешно сохранён.'

    def get(self, request, quiz_id):
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


@method_decorator(quiz_taken_required, name='dispatch')
class QuizRestartView(View):

    success_message = 'Результат успешно сброшен.'
    error_message =  'Произошла ошибка во время сброса результата.',

    def get(self, request, quiz_id):
        try:
            del request.session['taken_quizzes'][str(quiz_id)]
        except KeyError:
            messages.error(request, self.error_message)
        else:
            messages.success(request, self.success_message)
        finally:
            return redirect(QuizConfig.QUIZ_FORM_URL, quiz_id)


@method_decorator(quiz_taken_required, name='dispatch')
class QuizReportView(TemplateView):

    template_name = f'{QuizConfig.name}/quiz-report.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        quiz_id = self.kwargs.get('quiz_id')
        taken_quiz_data = self.request.session.get('taken_quizzes').get(str(quiz_id))

        quiz = get_object_or_404(Quiz, id=quiz_id)
        quiz.result = taken_quiz_data.get('result')

        questions = Question.objects.filter(quiz=quiz)
        for question in questions:
            question.correct_answer = question.get_correct_answer()
            question.user_answer = Answer.objects.get(
                id=taken_quiz_data.get('answers').get(str(question.id))
            )

        context['quiz'] = quiz
        context['questions'] = questions

        return context
