# -*- coding: utf-8 -*-

from ctx_defense import CTX
from flask import Markup
from cgi import escape


def ctx_processor():
    ctx_object = CTX()

    def ctx_protect(secret, origin=None, alphabet=None):
        protected_secret = ctx_object.protect(secret, origin, alphabet)
        return Markup(
            "<div data-ctx-origin='{origin_id}'>{permuted}</div>".format(
                origin_id=protected_secret['origin_id'],
                permuted=escape(protected_secret['permuted'])
                )
            )

    return {
        'ctx_protect': ctx_protect,
    }
