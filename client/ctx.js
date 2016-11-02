/* Generic base CTX library.
 * Exposes CTX inverse permutation for client-side processing. */

let CTX = {
    unpermute: function(permutation, permuted) {
        console.log('Unpermuting "' + permuted + '"\
                     by reversing permutation "' + permutation + '"');
        let secretAlphabet = permutation.split('').slice();
        secretAlphabet.sort();

        let secret = '';
        let inversePermutationMap = {};

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
        if (this.permutations.length <= idx) {
            console.log('CTX: Invalid permutation index: ' + idx + '. Skipping.');
            return;
        }

        let permutation = this.permutations[element.dataset.ctxOrigin];
        let permuted = element.innerHTML;
        let secret = CTX.unpermute(permutation, permuted);
        element.innerHTML = secret;
    },
    _getPermutedElements: function() {
        let divs = document.getElementsByTagName('div');
        let elements = [];

        for (let i = 0; i < divs.length; ++i) {
            let div = divs[i];
            if (typeof div.dataset.ctxOrigin !== 'undefined') {
                elements.push(div);
            }
        }

        return elements;
    },
    _getPermutations: function() {
        let permutationsElement = document.getElementById('ctx-permutations');

        if (permutationsElement == null) {
            throw 'CTX: No permutation translation table is available. Aborting.'
        }
        this.permutations = JSON.parse(permutationsElement.textContent);
        console.log('Recovered permutations table:');
        console.log(this.permutations);
    },
    process: function() {
        this._getPermutations();
        let elements = this._getPermutedElements();

        for (let i = 0; i < elements.length; ++i) {
            this._unpermuteElement(elements[i]);
        }
    }
};
