const shuffle = require('shuffle-array'),
      _ = require('lodash');


class CTX {
    constructor() {
        this.permuters = [];
        this.origins = {};
    }

    getPermutations() {
        let allpermuters = [];
        for (let i = 0; i < this.permuters.length; i++) {
            allpermuters[i] = this.permuters[i].getPermutation();
        };
        return allpermuters;
    }

    protect(secret, origin) {
        let permuter;
        let originId;

        if (typeof origin === 'undefined') {
            do {
                let possible = 'abcdefghijklmnopqrstuvwxyz';
                for (let i = 0; i < 10; i++)
                    origin += possible.charAt(Math.floor(Math.random() * possible.length));
            } while (typeof this.origins[origin] !== 'undefined');
        }

        if (typeof this.origins[origin] !== 'undefined') {
            originId = this.origins[origin];
            permuter = this.permuters[originId];
        }
        else {
            permuter = new AsciPrintable;
            originId = this.permuters.length;
            this.origins[origin] = originId;
            this.permuters.push(permuter);
        }

        let permuted = permuter.permute(secret);
        return {
            'origin_id': originId,
            'permuted': permuted
        }
    }
}

module.exports = CTX;
