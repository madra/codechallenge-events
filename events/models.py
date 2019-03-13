''' events models'''
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.core.validators import MinValueValidator
User = get_user_model()


class Event(models.Model):
    owner = models.ForeignKey(
        User,
        help_text="owner of event"
    )
    title = models.CharField(
        max_length=200,
        help_text="title of event"
    )
    description = models.TextField(
        help_text="description of event"
    )
    event_date = models.DateTimeField(
        help_text="The datetime of the event"

    )
    creation_date = models.DateTimeField(
        auto_now_add=True,
        help_text="The datetime event was created"
    )
    participants = models.PositiveIntegerField(
        help_text="The number of participants for this event",
        validators=[MinValueValidator(1)]
    )

    @models.permalink
    def url(self):
        return ('event_detail', ({self.pk}))

    @models.permalink
    def edit_url(self):
        return ('event_edit', ({self.pk}))

    @models.permalink
    def rsvp_url(self):
        return ('rsvp_event', ({self.pk}))

    @property
    def owner_name(self):
        '''
        the part of the email before the "@"
        '''
        return str(self.owner.email.split("@")[0])

    def clean(self, *args, **kwargs):
        super(Event, self).clean(*args, **kwargs)

        '''
        The date cannot be earlier than today
        '''
        if self.event_date < timezone.now():
            raise ValidationError(
                'Event date cannot be earlier than Today.'
            )

    @property
    def rsvp_num(self):
        """
        number of people who have rsvp'ed
        """
        return len(
            Rsvp.objects.filter(event=self)
        )

    @property
    def can_rsvp(self):
        """
        make sure that the rsvp count is not greate than participants
        """
        if self.rsvp_num >= self.participants:
            return False
        return True

    def user_has_rsvp(self, user):
        """
        check if a user has rsvp'ed this event
        """
        if len(Rsvp.objects.filter(event=self, user=user)) > 0:
            return True
        return False


class Rsvp(models.Model):
    user = models.ForeignKey(
        User,
        help_text="user who rsvp'ed"
    )
    event = models.ForeignKey(
        Event,
        help_text="event user rsvp'ed"
    )
    date = models.DateTimeField(
        auto_now_add=True,
        help_text="The datetime rsvp was added"

    )

    class Meta:
        unique_together = ("user", "event")
