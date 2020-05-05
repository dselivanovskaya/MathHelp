from django.conf import settings
from django.test import TestCase
from django.urls import reverse

from tests.data import MALE_USER

from tickets.apps import TicketsConfig
from tickets.models import Ticket


class TicketListViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        MALE_USER.create()
        cls.url = reverse(TicketsConfig.TICKET_LIST_URL)

    def test_anonymous_request_redirects_to_login_page(self):
        response = self.client.get(self.url)
        redirect_url = f'{reverse(settings.LOGIN_URL)}?next={self.url}'
        self.assertRedirects(response, redirect_url)

    def test_authenticated_request(self):
        self.client.login(username=MALE_USER.username, password=MALE_USER.password)
        self.assertEqual(self.client.get(self.url).status_code, 200)


class TicketDetailViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        MALE_USER.create()
        cls.ticket = Ticket.objects.create(name='ticket', level=4, filename='test.pdf')
        cls.url = cls.ticket.get_absolute_url()

    def test_anonymous_request_redirects_to_login_page(self):
        response = self.client.get(self.url)
        redirect_url = f'{reverse(settings.LOGIN_URL)}?next={self.url}'
        self.assertRedirects(response, redirect_url)

    def test_authenticated_request(self):
        self.client.login(username=MALE_USER.username, password=MALE_USER.password)
        self.assertEqual(self.client.get(self.url).status_code, 200)


class TicketPDFViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        MALE_USER.create()
        cls.ticket = Ticket.objects.create(name='ticket', level=4, filename='test.pdf')
        cls.url = cls.ticket.get_pdf_url()

    def test_anonymous_request_redirects_to_login_page(self):
        response = self.client.get(self.url)
        redirect_url = f'{reverse(settings.LOGIN_URL)}?next={self.url}'
        self.assertRedirects(response, redirect_url)

    def test_appends_ticket_id_to_session_read_tickets(self):
        self.client.login(username=MALE_USER.username, password=MALE_USER.password)
        self.client.get(self.url)
        self.assertEqual(self.client.session['read_tickets'], [self.ticket.id])
