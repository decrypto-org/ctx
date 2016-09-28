# -*- coding: utf-8 -*-

import ctx_defense
import unittest


class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.ctx = ctx_defense.CTX()
