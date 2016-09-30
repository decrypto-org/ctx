# -*- coding: utf-8 -*-

from unittest import TestCase
from flask_ctx.context_processors import ctx_processor


class AsciiprintableTestCase(TestCase):
    def setUp(self):
        self.processor = ctx_processor()
