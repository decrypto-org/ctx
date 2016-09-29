# -*- coding: utf-8 -*-

from ctx_defense import CTX


def ctx_protect(request):
    return {
        'ctx': CTX()
    }
