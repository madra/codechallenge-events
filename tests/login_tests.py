# tests/views.py
''' test login '''
# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test.client import Client
import unittest


class LoginTestCase(unittest.TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            'random', 'random@pass.com', 'randompass')

    def testLogin(self):
        self.client.login(username='random', password='randompass')
        response = self.client.get(reverse('auth_login')
                                   )
        self.assertEqual(response.status_code, 200)
