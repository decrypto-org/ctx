# -*- coding: utf-8 -*-

from unittest import TestCase
from flask_ctx.context_processors import ctx_processor
import re
from string import printable


class AsciiprintableTestCase(TestCase):
    def setUp(self):
        self.processor = ctx_processor()

    def test_protect(self):
        protected_tag = self.processor['ctx_protect']('secret', 'origin')
        regex = r"[{p}]*(<div data-ctx-origin=')(\d*)('>)([{p}]*)(</div>)[{p}]*".format(p=re.escape(printable))
        self.assertTrue(re.match(regex, protected_tag))
