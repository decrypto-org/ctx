# -*- coding: utf-8 -*-

from random import choice
from string import ascii_lowercase
from copy import deepcopy
from permuters import AsciiPrintablePermuter


class PermutationUnavailableError(Exception):
    '''Custom exception to handle cases when the secret alphabet parameter for CTX
    initialization does not correspond to an implemented permuter.'''
    pass


class CTX(object):
    '''The CTX defense class. Maintains the state of all generated permutations
    per origin and uses permuters for permutations on secret alphabets.

    Implements the following interface:
        available_permuters: Dictionary that defines the
            implemented permuters. The keys are strings that
            identify the secret alphabet and the values are classes that implement
            the following interface:
                get_permutation(), permute(secret).
        get_permutations(): Returns a list of strings, the i-th string being the
            generated permutation for the origin with origin_id = i.
        protect(secret, <origin>, <secret_alphabet>): Accepts one to three string
            parameters. If no *origin* is given, a random identifier of 10
            lowercase letters is generated. If no *secret_alphabet* is given,
            *ASCII_printable* is used by default. Applies the permutation that
            was generated for the *origin* on the *secret*. If *protect* is
            called for the first time for the *origin*, *secret_alphabet* must
            be set and exist in the keys of *available_permutation_permuters*.
            In this case, a permutation is generated for the *origin*. Returns
            a dictionary with the following fields:
                origin_id: An integer that identifies the *origin*.
                permuted: A string containing the permuted secret.'''
    available_permuters = {
        'ASCII_printable': AsciiPrintablePermuter
    }

    def __init__(self):
        self._permuters = []
        self._permutations = []
        self._origins = {}

    def get_permutations(self):
        return deepcopy(self._permutations)

    def protect(self, secret, origin=None, secret_alphabet=None):
        if type(secret) != str:
            secret = str(secret)
        try:
            if origin and type(origin) != str:
                origin = str(origin)
            origin_id = self._origins[origin]
            permuter = self._permuters[origin_id]
        except KeyError:
            try:
                if not secret_alphabet:
                    secret_alphabet = 'ASCII_printable'
                permuter = self.available_permuters[secret_alphabet]()
            except KeyError:
                raise PermutationUnavailableError('Permuter for given alphabet is not available.')
            origin_id = len(self._permuters)
            while not origin or origin in self._origins:
                origin = ''.join(choice(ascii_lowercase) for _ in range(10))
            self._origins[origin] = origin_id
            self._permuters.append(permuter)
            self._permutations.append(permuter.get_permutation())

        return {
            'origin_id': origin_id,
            'permuted': permuter.permute(secret)
        }
