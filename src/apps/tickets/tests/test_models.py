import os

from django.conf import settings
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse

from tickets.apps import TicketsConfig
from tickets.models import Ticket


class TicketModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.ticket = Ticket.create(name='ticket', level=2, filename='ticket.pdf')

    def test_objects_create_no_fields(self):
        ''' Can not create a Ticket without fields. '''
        with  self.assertRaises(TypeError):
            Ticket.objects.create()

    def test_objects_create_invalid_level_field(self):
        ''' Can not create a ticket with an invalid level value. '''
        error_message = Ticket.error_messages['invalid_level']
        with self.assertRaisesRegexp(ValidationError, error_message):
            Ticket.objects.create(name='ticket', level=25, filename='ticket.pdf')

    def test_get_absolute_url(self):
        self.assertEquals(
            self.ticket.get_absolute_url(),
            reverse(TicketsConfig.TICKET_DETAIL_URL, args=[self.ticket.id])
        )

    def test_get_pdf_url(self):
        self.assertEquals(
            self.ticket.get_pdf_url(),
            reverse(TicketsConfig.TICKET_PDF_URL, args=[self.ticket.filename])
        )

    def test_get_level_img_path(self):
        self.assertEquals(self.ticket.get_level_img_path(),
            os.path.join(TicketsConfig.name, 'img', f'{self.ticket.level}-star.png')
        )

    def test_get_pdf_path(self):
        self.assertEquals(self.ticket.get_pdf_path(),
             os.path.join(
                 settings.MEDIA_ROOT, TicketsConfig.name, 'pdf', self.ticket.filename
             )
        )
