from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.utils.decorators import method_decorator

from django.views import View
from django.views.generic import RedirectView
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView

from .apps import QuizConfig
from .decorators import quiz_taken_required, quiz_not_taken_required
from .forms import QuizForm
from .models import Quiz, Question, Answer, Result


@method_decorator(quiz_not_taken_required, name='dispatch')
class QuizFormView(FormView):

    form_class = QuizForm
    template_name = f'{QuizConfig.name}/quiz-form.html'

    def get_object(self):
        if not hasattr(self, 'object'):
            self.object = get_object_or_404(Quiz, id=self.kwargs['quiz_id'])
        return self.object

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['quiz'] = self.get_object()
        return context

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super().get_form_kwargs(*args, **kwargs)
        kwargs['quiz'] = self.get_object()
        return kwargs

    def form_valid(self, form):
        self.request.session.get('taken_quizzes').update({
            self.get_object().id: {
                'result':  form.cleaned_data['result'],
                'answers': form.cleaned_data['answers'],
                'is_saved':   False,
            }
        })
        return super().form_valid(form)

    def get_success_url(self):
        return self.get_object().get_result_url()


@method_decorator(quiz_taken_required, name='dispatch')
class QuizSaveView(View):

    success_message = 'Ваш результат был успешно сохранён.'

    def get(self, request, quiz_id):
        quiz = get_object_or_404(Quiz, id=quiz_id)
        quiz_session_data = request.session['taken_quizzes'][str(quiz_id)]

        Result.objects.update_or_create(
            quiz=quiz, user=request.user,
            defaults={'percent': quiz_session_data['result']},
        )

        quiz_session_data['is_saved'] = True
        messages.success(request, self.success_message)

        return redirect(self.request.user.profile.get_absolute_url())


@method_decorator(quiz_taken_required, name='dispatch')
class QuizRestartView(RedirectView):

    success_message = 'Результат был успешно сброшен.'

    def get_redirect_url(self, *args):
        quiz_id = self.kwargs['quiz_id']

        del self.request.session['taken_quizzes'][str(quiz_id)]
        messages.success(self.request, self.success_message)

        return reverse(QuizConfig.QUIZ_FORM_URL, args=[quiz_id])


@method_decorator(quiz_taken_required, name='dispatch')
class QuizResultView(TemplateView):

    template_name = f'{QuizConfig.name}/quiz-result.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        quiz = get_object_or_404(Quiz, id=self.kwargs['quiz_id'])
        taken_quizzes = self.request.session['taken_quizzes']

        quiz.result = taken_quizzes[str(quiz.id)]['result']
        quiz.is_saved = taken_quizzes[str(quiz.id)]['is_saved']

        context['quiz'] = quiz

        return context


@method_decorator(quiz_taken_required, name='dispatch')
class QuizReportView(TemplateView):

    template_name = f'{QuizConfig.name}/quiz-report.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        quiz_id = self.kwargs['quiz_id']
        quiz_session_data = self.request.session['taken_quizzes'][(str(quiz_id))]

        quiz = get_object_or_404(Quiz, id=quiz_id)
        quiz.result = quiz_session_data['result']

        for question in quiz.get_questions():
            user_answer_id = quiz_session_data['answers'][str(question.id)]
            question.user_answer = get_object_or_404(Answer, id=user_answer_id)

        context['quiz'] = quiz

        return context
