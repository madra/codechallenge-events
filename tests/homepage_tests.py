# tests/views.py
''' test homepage view'''
# -*- coding: utf-8 -*-
from django.http import HttpRequest
from django.test import SimpleTestCase


class HomePageTests(SimpleTestCase):

    def test_home_page_status_code(self):
        response = self.client.get('/')
        self.assertEquals(response.status_code, 200)
