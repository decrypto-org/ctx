# -*- coding: utf-8 -*-

import os

from django import setup
from django.test import TestCase
from django.test.client import RequestFactory

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_ctx.tests.settings")
setup()


class BaseTestCase(TestCase):
    def setUp(self):
        self.reqfactory = RequestFactory()
