import os

from django.conf import settings
from django.db import models
from django.urls import reverse

from .apps import TicketsConfig


class Ticket(models.Model):

    name = models.CharField(max_length=256, unique=True)
    level = models.SmallIntegerField()
    filename = models.CharField(max_length=256, unique=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse(TicketsConfig.TICKET_DETAIL_URL, args=[self.id])

    def get_absolute_pdf_url(self):
        return reverse(TicketsConfig.TICKET_PDF_URL, args=[self.filename])

    def get_absolute_img_path(self):
        return os.path.join('tickets', 'img', f'{self.level}-star.png')

    def get_absolute_pdf_path(self):
        ''' For TicketReadPDF View. '''
        return os.path.join(settings.MEDIA_ROOT, 'tickets', 'pdf', self.filename)
