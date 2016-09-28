# -*- coding: utf-8 -*-

import ctx_defense
from ctx_defense.app import PermutationUnavailableError
import unittest
from string import printable


class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.ctx = ctx_defense.CTX()

    def test_permutation_unavailable(self):
        try:
            self.ctx.protect('secret', 'origin', 'invalid alphabet')
        except PermutationUnavailableError:
            pass

    def test_default_alphabet(self):
        permuted = self.ctx.protect('secret', 'origin')
        origin_id = permuted['origin_id']
        permutation = self.ctx.get_permutations()[origin_id]
        self.assertEqual(set(printable), set(permutation))
