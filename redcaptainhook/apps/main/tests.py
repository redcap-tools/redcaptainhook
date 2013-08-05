"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse


class SimpleTest(TestCase):
    def setUp(self):
        self.c = Client()

    def test_index(self):
        r = self.c.get(reverse('index'))
        self.assertEqual(r.status_code, 200)

    def test_about(self):

        r = self.c.get(reverse('about'))
        self.assertEqual(r.status_code, 200)
