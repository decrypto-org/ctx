from collections import OrderedDict
from json import dumps

class CTX:
    def _generate_permutation(self):
        # Fisher-Yates
        return permutation

    def __init__(self):
        self._permutations = []
        self._origins = {}

    def getPermutations(self):
        return self._permutations

    def protect(self, secret, origin):
        try:
            origin_id = self._origins[origin]
            permutation = self._permutations[origin_id]
        except KeyError:
            permutation = self._generate_permutation()
            origin_id = len(self._permutations)
            self._origins[origin] = origin_id
            self._permutations.append(permutation)

        return {
            'origin_id': origin_id,
            'permuted': self.apply(permutation, secret)
        }

    def apply(self, permutation, secret):
        permuted_secret = map(permutation, secret)

        return permuted_secret

# Django

ctx = CTX()

def ctx_protect(secret, origin):
    protected = ctx.protect(secret, origin)

    return "<div data-ctx-origin='%s'>%s</div>" % \
            (protected['origin_id'], protected['permuted'])

def generate_json():
    permutations = ctx.getPermutations()

    return json.dumps(permutations)
