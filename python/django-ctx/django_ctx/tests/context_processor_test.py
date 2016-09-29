# -*- coding: utf-8 -*-

import os
import re

from django import setup
from django.test import TestCase
from django.test.client import RequestFactory
from django.template.response import TemplateResponse

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_ctx.tests.settings")
setup()


class BaseTestCase(TestCase):
    def setUp(self):
        self.reqfactory = RequestFactory()


class CtxprocessorTestCase(BaseTestCase):
    def test_context_variable(self):
        req = self.reqfactory.get('/')
        res = TemplateResponse(req, 'variable.html', {})
        res.render()
        regex = r"&lt;ctx_defense\.app\.CTX object at 0x[0-9a-f]*&gt;"
        self.assertTrue(
            re.match(regex, res.rendered_content)
        )
