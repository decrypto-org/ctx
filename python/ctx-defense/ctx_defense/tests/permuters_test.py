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
