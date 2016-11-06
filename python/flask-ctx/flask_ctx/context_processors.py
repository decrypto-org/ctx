# -*- coding: utf-8 -*-

from ctx_defense import CTX
from json import dumps
from flask import Markup
from urllib import quote


def ctx_processor():
    ctx_object = CTX()

    def ctx_protect(secret, origin=None, alphabet=None):
        protected_secret = ctx_object.protect(secret, origin, alphabet)
        return Markup(
            "<div data-ctx-origin='{origin_id}'>{permuted}</div>".format(
                origin_id=protected_secret['origin_id'],
                permuted=quote(protected_secret['permuted'])
            )
        )

    def ctx_permutations():
        return Markup(
            "<script type='application/json' id='ctx-permutations'>{permutations}</script>".format(
                permutations=dumps(
                    ctx_object.get_permutations()
                )
            )
        )

    return {
        'ctx_protect': ctx_protect,
        'ctx_permutations': ctx_permutations
    }
