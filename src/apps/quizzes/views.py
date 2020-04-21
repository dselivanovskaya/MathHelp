from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View

from tickets.models import Ticket

from .apps import QuizzesConfig as quizzes_config
from .forms import QuizForm
from .models import Quiz


class QuizTicketView(View):

    template_name = f'{quizzes_config.name}/quiz.html'
    form_class = QuizForm

    def get(self, request, ticket_id):
        ticket = get_object_or_404(Ticket, id=ticket_id)
        form = self.form_class(questions=ticket.quiz.question_set.all())
        return render(request, self.template_name, {'form': form, 'ticket': ticket})

    def post(self, request, ticket_id):
        ticket = get_object_or_404(Ticket, id=ticket_id)
        form = self.form_class(ticket.quiz.question_set.all(), request.POST)
        if form.is_valid():
            result = form.cleaned_data['result']
            if result < Quiz.MIN_REQUIRED_RESULT:
                messages.error(request, f'Ваш результат: {result}')
            else:
                messages.success(request, f'Ваш результат: {result}')
            return redirect(quizzes_config.QUIZ_TICKET_URL, ticket_id)
        return render(request, self.template_name, {'form': form, 'ticket': ticket})
