const shuffle = require('shuffle-array'),
      _ = require('lodash');

class AsciPrintable {
    constructor() {
        this.alphabet = [];
        this.permuter = [];
        this.dict = {};

        let asciiSpecialStart = 9;
        let asciiSpecialStop = 13;

        let asciiStart = 32;
        let asciiStop = 126;

        //alphabet array contains all ASCII symbols
        for (let i = asciiSpecialStart; i <= asciiSpecialStop; i++) {
            this.alphabet.push(String.fromCharCode(i));
        }

        for (let i = asciiStart; i <= asciiStop; i++) {
            this.alphabet.push(String.fromCharCode(i));
        }

        this.permuter = shuffle(this.alphabet.slice());
        this.dict = _.zipObject(this.alphabet, this.permuter);
    }

    getPermutation() {
        return this.permuter.join('');
    }

    permute(secret) {
        let permSecret = _.map(secret, (secretChar) => {
            return this.dict[secretChar];
        });
        return permSecret.join('');
    }
}

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

        try{
            if (typeof secret === 'undefined') throw 'Secret not set';
        }
        catch(err) {
            console.log(err);
            return;
        }

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
