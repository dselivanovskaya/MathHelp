import os

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse

from .apps import TicketsConfig


class TicketManager(models.Manager):

    def create(self, name, level, filename, **kwargs):
        ''' Validate all fields were given. Validate level field. '''

        if not (Ticket.MIN_LEVEL <= level <= Ticket.MAX_LEVEL):
            raise ValidationError(Ticket.error_messages['invalid_level'])

        return super().create(name=name, level=level, filename=filename, **kwargs)


class Ticket(models.Model):

    MIN_LEVEL, MAX_LEVEL = 1, 5

    error_messages = {
        'invalid_level': f'Level must be a value from {MIN_LEVEL} to {MAX_LEVEL}.'
    }

    name = models.CharField(max_length=256, unique=True)
    level = models.SmallIntegerField()
    filename = models.CharField(max_length=256, unique=True)

    objects = TicketManager()

    def __str__(self):
        return self.name

    @property
    def level_img_path(self):
        return os.path.join(TicketsConfig.name, 'img', f'{self.level}-star.png')

    @property
    def pdf_path(self):
        return os.path.join(settings.MEDIA_ROOT, TicketsConfig.name, 'pdf', self.filename)

    def get_absolute_url(self):
        return reverse(TicketsConfig.TICKET_DETAIL_URL, args=[self.id])

    def get_pdf_url(self):
        return reverse(TicketsConfig.TICKET_PDF_URL, args=[self.filename])

    def get_quiz_url(self):
        if hasattr(self, 'quiz'):
            return self.quiz.get_absolute_url()

    def get_pdf(self):
        ''' Return ticket's pdf file. '''
        return open(self.pdf_path, 'rb')

    def get_comments(self):
        ''' Return tickets's forum comments. '''
        return self.comment_set.all()
