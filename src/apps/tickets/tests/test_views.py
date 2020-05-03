from django.test import TestCase
from django.urls import reverse

from tests.data import USER_MALE

from tickets.apps import TicketsConfig
from tickets.models import Ticket


class TicketListViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.url = reverse(TicketsConfig.TICKET_LIST_URL)
        USER_MALE.create_in_db()

    def test_anonymous_request(self):
        self.assertEqual(self.client.get(self.url).status_code, 302)

    def test_authenticated_request(self):
        self.client.login(username=USER_MALE.username, password=USER_MALE.password)
        self.assertEqual(self.client.get(self.url).status_code, 200)


class TicketDetailViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.ticket = Ticket.objects.create(
            name='New ticket', level=4, filename='new-ticket.pdf'
        )
        cls.url = cls.ticket.get_absolute_url()
        USER_MALE.create_in_db()

    def test_anonymous_request(self):
        self.assertEqual(self.client.get(self.url).status_code, 302)

    def test_authenticated_request(self):
        self.client.login(username=USER_MALE.username, password=USER_MALE.password)
        self.assertEqual(self.client.get(self.url).status_code, 200)


class TicketPDFViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.ticket = Ticket.objects.create(
            name='New ticket', level=4, filename='new-ticket.pdf'
        )
        cls.url = cls.ticket.get_absolute_pdf_url()
        USER_MALE.create_in_db()

    def test_anonymous_request(self):
        self.assertEqual(self.client.get(self.url).status_code, 302)
