# -*- coding: utf-8 -*-

from django import template
from json import dumps
from urllib import quote

register = template.Library()


@register.inclusion_tag('ctx/protected.html', takes_context=True)
def ctx_protect(context, secret, origin=None, alphabet=None):
    try:
        ctx = context['ctx']
    except KeyError:
        raise KeyError('ctx not in Template context. Is the context processor for ctx properly set?')

    protected_secret = ctx.protect(secret, origin, alphabet)

    return {
        'permuted': quote(protected_secret['permuted']),
        'origin_id': protected_secret['origin_id']
    }


@register.inclusion_tag('ctx/permutations.html', takes_context=True)
def ctx_permutations(context):
    try:
        ctx = context['ctx']
    except KeyError:
        raise KeyError('ctx not in Template context. Is the context processor for ctx properly set?')
    return {
        'permutations': dumps(
            ctx.get_permutations()
        )
    }
