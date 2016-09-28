# -*- coding: utf-8 -*-

import ctx_defense
from ctx_defense.app import PermutationUnavailableError
import unittest


class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.ctx = ctx_defense.CTX()

    def test_permutation_unavailable(self):
        try:
            self.ctx.protect('secret', 'origin', 'invalid alphabet')
        except PermutationUnavailableError:
            pass
