# -*- coding: utf-8 -*-

import ctx_defense.permuters
import unittest


class AsciiprintableTestCase(unittest.TestCase):
    def setUp(self):
        self.permuter = ctx_defense.permuters.AsciiPrintablePermuter()
