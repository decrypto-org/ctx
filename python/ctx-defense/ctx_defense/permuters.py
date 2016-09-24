# -*- coding: utf-8 -*-

from string import printable
from random import shuffle


class AsciiPrintablePermuter(object):
    '''A permutation generator for the alphabet that includes all ASCII
    printable characters.

    Implements the following interface:
        get_permutation(): Returns a string containing the generated
            permutation for the alphabet.
        permute(secret): Accepts a string parameter, applies the generated
            permutation on each character and returns the permuted data.'''
    def __init__(self):
        self._permutation, self._permutation_dict = self._generate_permutation()

    def _generate_permutation(self):
        alphabet_list = list(printable)
        shuffle(alphabet_list)
        permutation = ''.join(alphabet_list)
        permutation_dict = {}
        for index, item in enumerate(permutation):
            permutation_dict[printable[index]] = item
        return permutation, permutation_dict

    def get_permutation(self):
        return self._permutation

    def permute(self, secret):
        return ''.join(
            map(lambda secret_char: self._permutation_dict[secret_char], secret)
        )
