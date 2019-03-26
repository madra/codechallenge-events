# tests/views.py
''' test login '''
# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from events.models import Event, Rsvp
from django.test.client import Client
import unittest
from django.utils import timezone


class EventTestCase(unittest.TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            'randomuser', 'randomuser@pass.com', 'randomuserpass'
        )
        self.user2 = User.objects.create_user(
            'randomuser1', 'randomuser1@pass.com', 'randomuser1pass'
        )
        self.user3 = User.objects.create_user(
            'randomuser2', 'randomuser2@pass.com', 'randomuser2pass'
        )
        self.event = Event.objects.create(
            owner=self.user,
            title="foo bar",
            event_date=timezone.now(),
            description="foo bar",
            participants=1
        )

    def test_owner_can_rsvp(self):
        rsvp = Rsvp(
            user=self.user,
            event=self.event
        )
        self.assertFalse(rsvp.save())

    def test_user_can_rsvp(self):
        rsvp = Rsvp(
            user=self.user2,
            event=self.event
        )
        self.assertTrue(rsvp.save())
