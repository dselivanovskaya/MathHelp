import os

from django.conf import settings
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse

from tests.data import USER_MALE

from tickets.apps import TicketsConfig
from tickets.models import Ticket


class TicketModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.model = Ticket
        cls.ticket = cls.model.objects.create(
            name='Ticket name', level=5, filename='ticket.pdf'
        )

    def test_objects_create(self):
        ''' Can not create a Ticket without fields. '''
        with  self.assertRaises(TypeError):
            self.model.objects.create()

    def test_ticket_save(self):
        ''' Can not save a ticket with an invalid level value. '''
        error_message = self.model.error_messages['invalid_level']
        with self.assertRaisesRegexp(ValidationError, error_message):
            self.model.objects.create(
                name='New ticket', level=25, filename='ticket.pdf'
            )

    def test_get_absolute_url(self):
        self.assertEquals(
            self.ticket.get_absolute_url(),
            reverse(TicketsConfig.TICKET_DETAIL_URL, args=[self.ticket.id])
        )

    def test_pdf_url(self):
        self.assertEquals(
            self.ticket.pdf_url,
            reverse(TicketsConfig.TICKET_PDF_URL, args=[self.ticket.filename])
        )

    def test_level_img_path(self):
        self.assertEquals(self.ticket.level_img_path,
            os.path.join(TicketsConfig.name, 'img', f'{self.ticket.level}-star.png')
        )

    def test_pdf_path(self):
        self.assertEquals(self.ticket.pdf_path,
             os.path.join(
                 settings.MEDIA_ROOT, TicketsConfig.name, 'pdf', self.ticket.filename
             )
        )
