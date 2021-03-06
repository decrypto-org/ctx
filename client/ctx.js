/* Generic base CTX library.
 * Exposes CTX inverse permutation for client-side processing. */

let CTX = {
    unpermute: function(permutation, permuted) {
        // console.log('Unpermuting "' + permuted + '"\
        //              by reversing permutation "' + permutation + '"');
        let secretAlphabet = permutation.split('').slice();
        secretAlphabet.sort();

        let secret = '';
        let inversePermutationMap = {};

        // inversePermutationMap = _.zipObject(permutation, secretAlphabet)
        for (let i = 0; i < secretAlphabet.length; ++i) {
            inversePermutationMap[permutation[i]] = secretAlphabet[i];
        }

        for (let i = 0; i < permuted.length; ++i) {
            secret += inversePermutationMap[permuted[i]];
        }

        return secret;
    },
};

/* HTML-specific CTX library.
 * Applies the inverse CTX permutation on HTML secrets stored in div tags.
 * Reads forward permutation table from application/json. */
let CTXHTML = {
    permutations: [],
    _unpermuteElement: function(element) {
        let idx = element.dataset.ctxOrigin;

        if (idx >= this.permutations.length) {
            // console.log('CTX: Invalid permutation index: ' + idx + '. Skipping.');
            return;
        }

        let permutation = this.permutations[idx];
        let permuted = element.innerHTML;
        // console.log('Permuted secret: ', permuted);
        permuted = decodeURIComponent(permuted);
        // console.log('Decoded permuted secret: ', permuted);
        let secret = CTX.unpermute(permutation, permuted);
        element.innerHTML = secret;
    },
    _getPermutedElements: function() {
        return document.querySelectorAll('div[data-ctx-origin]');
    },
    _getPermutations: function() {
        let permutationsElement = document.getElementById('ctx-permutations');

        if (permutationsElement == null) {
            throw 'CTX: No permutation translation table is available. Aborting.'
        }
        this.permutations = JSON.parse(permutationsElement.textContent);
        // console.log('Recovered permutations table:');
        // console.log(this.permutations);
    },
    process: function() {
        this._getPermutations();
        let elements = this._getPermutedElements();

        for (let i = 0; i < elements.length; ++i) {
            this._unpermuteElement(elements[i]);
        }
    }
};

document.addEventListener('DOMContentLoaded', CTXHTML.process.bind(CTXHTML));
