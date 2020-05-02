from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse

from tickets.models import Ticket

from .apps import QuizConfig


class Quiz(models.Model):
    PASS_PERCENT = 70

    ticket = models.OneToOneField(Ticket, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'quizzes'  # for admin panel

    def __str__(self):
        return self.ticket.name

    def get_absolute_url(self):
        return reverse(QuizConfig.QUIZ_TICKET_URL, args=[self.id])



class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    text = models.CharField(max_length=512)

    def __str__(self):
       return self.text

    def get_correct_answer(self):
        ''' Return the correct answer for particularr question. '''
        for answer in Answer.objects.filter(question=self):
            if answer.is_correct:
                return answer


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.CharField(max_length=512)
    is_correct = models.BooleanField()

    def __str__(self):
        return self.text


class Result(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    percent = models.PositiveSmallIntegerField()

    def __str__(self):
        return f'{self.user.username}: {self.quiz.ticket}'


