from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse

from tests.data import MALE_USER

from tickets.models import Ticket

from quiz.apps import QuizConfig
from quiz.models import Quiz, Question, Answer, Result


class QuizModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        ticket = Ticket.objects.create(name='test', level=5, filename='test.pdf')
        cls.instance = Quiz.objects.create(ticket=ticket)

    def test_str(self):
        self.assertEquals(str(self.instance), str(self.instance.ticket))

    def test_get_absolute_url(self):
        url = reverse(QuizConfig.QUIZ_FORM_URL, args=[self.instance.id])
        self.assertEquals(self.instance.get_absolute_url(), url)

    def test_get_result_url(self):
        url = reverse(QuizConfig.QUIZ_RESULT_URL, args=[self.instance.id])
        self.assertEquals(self.instance.get_result_url(), url)

    def test_get_save_url(self):
        url = reverse(QuizConfig.QUIZ_SAVE_URL, args=[self.instance.id])
        self.assertEquals(self.instance.get_save_url(), url)

    def test_get_restart_url(self):
        url = reverse(QuizConfig.QUIZ_RESTART_URL, args=[self.instance.id])
        self.assertEquals(self.instance.get_restart_url(), url)

    def test_get_report_url(self):
        url = reverse(QuizConfig.QUIZ_REPORT_URL, args=[self.instance.id])
        self.assertEquals(self.instance.get_report_url(), url)


class QuestionModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        ticket = Ticket.objects.create(name='test', level=5, filename='test.pdf')
        quiz = Quiz.objects.create(ticket=ticket)
        cls.instance = Question.objects.create(quiz=quiz, text='test')
        cls.correct_answer = Answer.objects.create(question=cls.instance,
                                                   text='test', is_correct=True)

    def test_str(self):
        self.assertEquals(str(self.instance), self.instance.text)

    def test_get_correct_answer(self):
        self.assertEqual(self.instance.get_correct_answer(), self.correct_answer)


class AnswerModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        ticket = Ticket.objects.create(name='test', level=5, filename='test.pdf')
        quiz = Quiz.objects.create(ticket=ticket)
        question = Question.objects.create(quiz=quiz, text='test')
        cls.instance = Answer.objects.create(question=question, text='test',
                                             is_correct=False)

    def test_str(self):
        self.assertEquals(str(self.instance), self.instance.text)


class ResultModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = MALE_USER.create()
        ticket = Ticket.objects.create(name='test', level=5, filename='test.pdf')
        cls.quiz = Quiz.objects.create(ticket=ticket)
        cls.instance = Result.objects.create(quiz=cls.quiz, user=cls.user, percent=25)

    def test_str(self):
        string =  f'{self.instance.user.username}: {self.instance.quiz.ticket}'
        self.assertEquals(str(self.instance), string)

    def test_create_with_invalid_percent_field(self):
        error_message = 'Invalid percent value'
        with self.assertRaisesRegexp(ValidationError, error_message):
            Result.objects.create(quiz=self.quiz, user=self.user, percent=245)

    def test_ticket_name(self):
        self.assertEqual(self.instance.ticket_name, self.instance.quiz.ticket.name)
