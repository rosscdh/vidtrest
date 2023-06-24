# -*- coding: UTF-8 -*-
from django.test import TestCase, Client


class BaseTestCase(TestCase):
    #fixtures = []

    def setUp(self):
        self.c = Client()
