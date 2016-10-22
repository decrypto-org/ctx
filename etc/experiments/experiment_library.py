# -*- coding: utf-8 -*-

import os
import random
import gzip
import string
from time import time
from json import dumps
from cgi import escape
from random import shuffle

from ctx_defense import CTX

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RESULTS_DIR = os.path.join(BASE_DIR, 'results')
if not os.path.exists(RESULTS_DIR):
        os.makedirs(RESULTS_DIR)

ENGLISH_TEXT = 'cleared_social_network'


def ctx_protect(ctx_object, secret, origin=None, alphabet=None):
    protected_secret = ctx_object.protect(secret, origin, alphabet)
    return "<div data-ctx-origin='{origin_id}'>{permuted}</div>".format(
        origin_id=protected_secret['origin_id'],
        permuted=escape(protected_secret['permuted'])
    )


def ctx_permutations(ctx_object):
    return "<script type='application/json' id='ctx-permutations'>{permutations}</script>".format(
        permutations=dumps(
            ctx_object.get_permutations()
        )
    )


def create_random_secret(length):
    return ''.join([random.choice(string.printable) for _ in range(length)])


def create_printable_secret(length):
    alphabet_list = list(string.printable)
    shuffle(alphabet_list)
    alphabet = ''.join(alphabet_list)
    secret = ''
    while len(secret) < length:
        secret += alphabet[len(secret) % len(alphabet)]
    return secret


def create_english_secret(length):
    with open(ENGLISH_TEXT, 'r') as f:
        english_text = f.read()
    secret_start = random.randint(0, len(english_text)-length)
    return english_text[secret_start:secret_start+length]


def test(origin_len, secret_len, secrets_per_origin=1, mode='random'):
    create_secret = {
        'random': create_random_secret,
        'printable': create_printable_secret,
        'english': create_english_secret,
    }
    origins = ['origin'+str(i) for i in range(origin_len)]
    aggr = []
    for i, _ in enumerate(origins):
        for _ in range(secrets_per_origin):
            aggr.append(
                (create_secret[mode](secret_len), origins[i])
            )

    t = time()
    c = CTX()
    protected = []
    for item in aggr:
        protected.append(ctx_protect(c, item[0], item[1]))
    protected.append(ctx_permutations(c))
    return time() - t, protected, [a[0] for a in aggr]


def file_write(identification, lst):
    with open(os.path.join(RESULTS_DIR, identification), 'w') as f:
        f.write(''.join(lst))


def zip_file_write(identification, lst):
    with gzip.open(os.path.join(RESULTS_DIR, '{}.gz'.format(identification)), 'wb') as f:
        f.write(''.join(lst))
