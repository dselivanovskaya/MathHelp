from django.test import TestCase

from tests.data import MALE_USER

from tickets.models import Ticket

from quiz.forms import QuizForm
from quiz.models import Quiz, Question, Answer


class QuizFormTest(TestCase):

    @classmethod
    def setUpTestData(cls):

        MALE_USER.create()
        ticket = Ticket.create(name='ticket', level=4, filename='ticket.pdf')
        quiz = Quiz.create(ticket=ticket)
        question =Question.create(quiz=quiz, text='sample')
        answer = Answer.create(question=question, text='answer', is_correct=True)

        cls.quiz = quiz
        cls.action_url = quiz.get_absolute_url()

    def setUp(self):
        self.client.login(username=MALE_USER.username, password=MALE_USER.password)

    def test_empty_form_returns_error(self):
        ''' Empty form submission should return an error. '''
        response = self.client.post(self.action_url, {})
        error_field = str(self.quiz.get_questions().first().id)
        error_message = 'This field is required.'
        self.assertFormError(response, 'form', error_field, error_message)
