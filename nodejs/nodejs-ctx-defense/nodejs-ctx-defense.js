const ctx = require('ctx-defense');

module.exports = {
    createCtxObject: function() {

        let ctxDefense = new ctx();
        return {
            ctxProtect: function(secret, origin) {
                let protect = ctxDefense.protect(secret, origin);
                return '<div data-ctx-origin=\'' + protect.origin_id + '\'>' +
                    encodeURIComponent(protect.permuted) + '</div>';
            },
            ctxPermutations: function() {
                let permutations = ctxDefense.getPermutations();
                return '<script type="application/json" id="ctx-permutations">' +
                    JSON.stringify(permutations) + '</script>';
            }
        };
    }
};
