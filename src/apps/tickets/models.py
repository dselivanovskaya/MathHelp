import os

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse

from .apps import TicketsConfig


class TicketManager(models.Manager):

    def create(self, name, level, filename, **kwargs):
        ''' Ensure name, level and filename are given. '''
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

    def save(self, *args, **kwargs):
        ''' Validate ticket level. '''
        if not (self.MIN_LEVEL <= self.level <= self.MAX_LEVEL):
            raise ValidationError(self.error_messages['invalid_level'])
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse(TicketsConfig.TICKET_DETAIL_URL, args=[self.id])

    @property
    def pdf_url(self):
        return reverse(TicketsConfig.TICKET_PDF_URL, args=[self.filename])

    @property
    def quiz_url(self):
        if hasattr(self, 'quiz'):
            return self.quiz.get_absolute_url()

    @property
    def level_img_path(self):
        return os.path.join(TicketsConfig.name, 'img', f'{self.level}-star.png')

    @property
    def pdf_path(self):
        return os.path.join(settings.MEDIA_ROOT, TicketsConfig.name, 'pdf', self.filename)

    @property
    def pdf(self):
        ''' Return ticket's pdf file. '''
        return open(self.pdf_path, 'rb')

    @property
    def comments(self):
        ''' Return tickets's forum comments. '''
        return self.comment_set.all()
