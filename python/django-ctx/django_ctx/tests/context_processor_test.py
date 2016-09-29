# -*- coding: utf-8 -*-

import os

from django import setup

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_ctx.tests.settings")
setup()
