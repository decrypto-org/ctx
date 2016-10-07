const {createCtxObject} = require('../nodejs-ctx-defense');

describe('nodejs-ctx-defense', () =>  {
   
    let ctx;
    beforeEach(function() {
        ctx = createCtxObject();
    });

    it('returns a div tag with the permuted secret', () => {
        let permuted = ctx.ctxProtect('secret');
        let regex =  /<div data-ctx-origin='\d*'>[\x00-\x7F]*<\/div>/
        expect(permuted).toMatch(regex);
    });
});
