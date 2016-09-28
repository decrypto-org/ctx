# -*- coding: utf-8 -*-

import ctx_defense
from ctx_defense.app import PermutationUnavailableError
import unittest
from string import printable


class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.ctx = ctx_defense.CTX()

    def test_permutation_unavailable(self):
        try:
            self.ctx.protect('secret', 'origin', 'invalid alphabet')
        except PermutationUnavailableError:
            pass

    def test_default_alphabet(self):
        permuted = self.ctx.protect('secret', 'origin')
        origin_id = permuted['origin_id']
        permutation = self.ctx.get_permutations()[origin_id]
        self.assertEqual(set(printable), set(permutation))

    def test_default_origin(self):
        permuted_1 = self.ctx.protect('secret')
        permuted_2 = self.ctx.protect('secret')
        permutations = self.ctx.get_permutations()
        self.assertNotEqual(permutations[permuted_1['origin_id']], permutations[permuted_2['origin_id']])

    def test_same_origin_different_secret(self):
        origin = 'origin'
        secret_1 = '1234'
        secret_2 = '2143'
        permuted_1 = self.ctx.protect(secret_1, origin)
        permuted_2 = self.ctx.protect(secret_2, origin)
        self.assertEqual(permuted_1['origin_id'], permuted_2['origin_id'])

    def test_same_origin_same_secret(self):
        origin = 'origin'
        secret = '1234'
        permuted_1 = self.ctx.protect(secret, origin)
        permuted_2 = self.ctx.protect(secret, origin)
        self.assertEqual(permuted_1['permuted'], permuted_2['permuted'])

    def test_different_origin(self):
        origin_1 = 'origin_1'
        origin_2 = 'origin_2'
        secret = '1234'
        permuted_1 = self.ctx.protect(secret, origin_1)
        permuted_2 = self.ctx.protect(secret, origin_2)
        self.assertNotEqual(permuted_1['origin_id'], permuted_2['origin_id'])
