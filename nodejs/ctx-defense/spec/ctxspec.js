ctx = require('../ctx');

describe('CTX', () =>  {

    let FakeCTX = new ctx();

    it('generates unique origin if not defined', () => {
        let permuted1 = FakeCTX.protect('secret');
        let permuted2 = FakeCTX.protect('secret');
        let permutations  = FakeCTX.getPermutations();
        expect(permutations[permuted1.origin_id]).not.toEqual(permutations[permuted2.origin_id]);
    });

    it('returns the same permutation for different secrets of the same origin', () => {
        let permuted1 = FakeCTX.protect('secret','bob');
        let permuted2 = FakeCTX.protect('newsecret','bob');
        let permutations  = FakeCTX.getPermutations();
        expect(permuted1.origin_id).toEqual(permuted2.origin_id);
    });

    it('returns the same permutation for the same secret for the same origin', () => {
        let permuted1 = FakeCTX.protect('secret','bob');
        let permuted2 = FakeCTX.protect('secret','bob');
        let permutations  = FakeCTX.getPermutations();
        expect(permuted1.permuted).toEqual(permuted2.permuted);
    });

    it('returns different permutation for the same secret of different origins', () => {
        let permuted1 = FakeCTX.protect('secret','bob');
        let permuted2 = FakeCTX.protect('secret','alice');
        let permutations  = FakeCTX.getPermutations();
        expect(permuted1.origin_id).not.toEqual(permuted2.origin_id);
    });

});
