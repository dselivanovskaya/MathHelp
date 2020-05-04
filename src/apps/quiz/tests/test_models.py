from django.test import TestCase
from django.urls import reverse

from tickets.models import Ticket

from quiz.apps import QuizConfig
from quiz.models import Quiz


class QuizModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        ticket = Ticket.create(name='ticket', level=5, filename='ticket.pdf')
        cls.quiz = Quiz.create(ticket=ticket)

    def test_get_absolute_url(self):
        self.assertEquals(
            self.quiz.get_absolute_url(),
            reverse(QuizConfig.QUIZ_FORM_URL, args=[self.quiz.id])
        )

    def test_get_save_url(self):
        self.assertEquals(
            self.quiz.get_save_url(),
            reverse(QuizConfig.QUIZ_SAVE_URL, args=[self.quiz.id])
        )

    def test_get_restart_url(self):
        self.assertEquals(
            self.quiz.get_restart_url(),
            reverse(QuizConfig.QUIZ_RESTART_URL, args=[self.quiz.id])
        )

    def test_get_report_url(self):
        self.assertEquals(
            self.quiz.get_report_url(),
            reverse(QuizConfig.QUIZ_REPORT_URL, args=[self.quiz.id])
        )
