from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse

from tickets.models import Ticket

from .apps import QuizConfig


class Quiz(models.Model):

    PASS_PERCENT = 70

    ticket = models.OneToOneField(Ticket, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'quizzes'

    def __str__(self):
        return str(self.ticket)

    def get_absolute_url(self):
        return reverse(QuizConfig.QUIZ_FORM_URL, args=[self.id])

    def get_result_url(self):
        return reverse(QuizConfig.QUIZ_RESULT_URL, args=[self.id])

    def get_save_url(self):
        return reverse(QuizConfig.QUIZ_SAVE_URL, args=[self.id])

    def get_restart_url(self):
        return reverse(QuizConfig.QUIZ_RESTART_URL, args=[self.id])

    def get_report_url(self):
        return reverse(QuizConfig.QUIZ_REPORT_URL, args=[self.id])

    def get_questions(self):
        if not hasattr(self, '_questions'):
            self._questions = self.question_set.all()
        return self._questions



class Question(models.Model):

    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    text = models.CharField(max_length=512, unique=True)

    def __str__(self):
       return self.text

    def get_correct_answer(self):
        ''' Return the correct answer for particularr question. '''
        if not hasattr(self, '_correct_answer'):
            self._correct_answer = self.answer_set.get(is_correct=True)
        return self._correct_answer


class Answer(models.Model):

    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.CharField(max_length=512, unique=True)
    is_correct = models.BooleanField()

    def __str__(self):
        return self.text


class ResultManager(models.Manager):

    def create(self, quiz, user, percent, **kwargs):
        ''' Validate percent field value. '''
        if not (0 <= percent <= 100):
            raise ValidationError('Invalid percent value.')
        return super().create(quiz=quiz, user=user, percent=percent, **kwargs)


class Result(models.Model):

    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    percent = models.PositiveSmallIntegerField()

    objects = ResultManager()

    def __str__(self):
        return f'{self.user.username}: {self.quiz.ticket}'

    @property
    def ticket_name(self):
        return self.quiz.ticket.name
