from django.db import models

from tickets.models import Ticket


class Quiz(models.Model):

    MIN_REQUIRED_RESULT = 70

    ticket = models.OneToOneField(Ticket, on_delete=models.CASCADE)
    questions_count = models.PositiveIntegerField()

    def __str__(self):
        return self.ticket.name

class Question(models.Model):
    text = models.CharField(max_length=1024)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)

    def __str__(self):
       return self.text

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    correct = models.BooleanField()
    text = models.CharField(max_length=512)

    def __str__(self):
        return self.text
