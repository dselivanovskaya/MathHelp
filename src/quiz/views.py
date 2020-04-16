from django.shortcuts import render, get_object_or_404, redirect, reverse

from django.contrib import messages
from django.views import View

from tickets.models import Ticket

from .forms import QuizForm


class TicketQuizView(View):

    template_name = 'quiz/quiz.html'
    form_class = QuizForm

    def get(self, request, id):
        ticket = get_object_or_404(Ticket, id=id)
        form = self.form_class(questions=ticket.quiz.question_set.all())
        return render(request, self.template_name, {'form': form, 'ticket': ticket})

    def post(self, request, id):
        ticket = get_object_or_404(Ticket, id=id)
        form = self.form_class(ticket.quiz.question_set.all(), request.POST)
        if form.is_valid():
            result = form.cleaned_data['result']
            messages.info(request, f'Result is {result}')
            return redirect(reverse('ticket-quiz', args=[id]))
        return render(request, self.template_name, {'form': form, 'ticket': ticket})