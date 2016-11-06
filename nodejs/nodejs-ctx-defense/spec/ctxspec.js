const {createCtxObject} = require('../nodejs-ctx-defense');

describe('nodejs-ctx-defense', () =>  {

    let ctx;
    beforeEach(function() {
        ctx = createCtxObject();
    });

    it('returns a div tag with the permuted secret', () => {
        let permuted = ctx.ctxProtect('secret');
        let regex =  /<div data-ctx-origin='\d*'>[\x00-\x7F]*<\/div>/;
        expect(permuted).toMatch(regex);
    });

    it('returns a script tag with an empty permutations list', () => {
        let permutations = ctx.ctxPermutations();
        let regex =  /<script type="application\/json" id="ctx-permutations">\[\]<\/script>/;
        expect(permutations).toMatch(regex);
    });

    it('returns a script tag with one element permutations list', () => {
        let permuted = ctx.ctxProtect('secret', 'user1');
        let permutations = ctx.ctxPermutations();
        let regex =  /<script type="application\/json" id="ctx-permutations">[[\x00-\x7F]*]<\/script>/;
        expect(permutations).toMatch(regex);
    });

    it('returns a script tag with multiple elements permutations list', () => {
        let permuted = ctx.ctxProtect('secret', 'user1');
        let permuted2 = ctx.ctxProtect('secret', 'user2');
        let permutations = ctx.ctxPermutations();
        let regex =  /<script type="application\/json" id="ctx-permutations">[[\x00-\x7F]*][[\x00-\x7F]*]<\/script>/;
        expect(permutations).toMatch(regex);
    });
});
