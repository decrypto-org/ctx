# -*- coding: utf-8 -*-

import ctx_defense.permuters
import unittest
from string import printable


class AsciiprintableTestCase(unittest.TestCase):
    def setUp(self):
        self.permuter = ctx_defense.permuters.AsciiPrintablePermuter()

    def test_permutation(self):
        permutation = self.permuter.get_permutation()
        self.assertEqual(set(printable), set(permutation))

    def test_same_secret(self):
        secret = 'secret'
        permuted_1 = self.permuter.permute(secret)
        permuted_2 = self.permuter.permute(secret)
        self.assertEqual(permuted_1, permuted_2)
