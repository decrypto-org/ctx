# -*- coding: utf-8 -*-

import os
import re

from django import setup
from django.test import TestCase
from django.test.client import RequestFactory
from django.template.response import TemplateResponse

from string import printable

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


class AsciiprintableTestCase(BaseTestCase):
    def test_protect_tag(self):
        req = self.reqfactory.get('/')
        res = TemplateResponse(req, 'protect.html', {})
        regex = r"(<div data-ctx-origin=')(\d*)('>)([{p}]*)(</div>)\n\n".format(p=re.escape(printable))
        self.assertTrue(
            re.match(regex, res.rendered_content)
        )

    def test_permutations_tag(self):
        req = self.reqfactory.get('/')
        res = TemplateResponse(req, 'permutations.html', {})
        regex = r"(<script type='application\/json' id='ctx-permutations'>\[)([{p}]*)(\]<\/script>)\n\n".format(p=re.escape(printable))
        self.assertTrue(
            re.match(regex, res.rendered_content)
        )

    def test_protected_permutation(self):
        req = self.reqfactory.get('/')
        res = TemplateResponse(req, 'full_page.html', {})
        protected = r"\n(<div data-ctx-origin=')(\d*)('>)([{p}]*)(</div>)\n\n".format(p=re.escape(printable))
        permutations = r"(<script type='application\/json' id='ctx-permutations'>\[)([{p}]*)(\]<\/script>)\n\n".format(p=re.escape(printable))
        regex = protected + permutations
        self.assertTrue(
            re.match(regex, res.rendered_content)
        )
