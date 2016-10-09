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

    def test_empty_permutations(self):
        regex = r"[{p}]*(<script type='application\/json' id='ctx-permutations'>\[\]<\/script>)[{p}]*".format(p=re.escape(printable))
        permutations_tag = self.processor['ctx_permutations']()
        self.assertTrue(re.match(regex, permutations_tag))

    def test_permutations_with_protected(self):
        regex = r"[{p}]*(<script type='application\/json' id='ctx-permutations'>\[)([{p}]*)(\]<\/script>)[{p}]*".format(p=re.escape(printable))

        # Test permutations with one entry
        self.processor['ctx_protect']('secret', 'origin')
        permutations_tag = self.processor['ctx_permutations']()
        self.assertTrue(re.match(regex, permutations_tag))

        # Test permutations with two entries
        self.processor['ctx_protect']('secret', 'origin')
        permutations_tag = self.processor['ctx_permutations']()
        self.assertTrue(re.match(regex, permutations_tag))
