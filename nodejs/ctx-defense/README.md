# ctx

The CTX defense library in javascript.

## Installation

npm install ctx-defense

## Basic Usage 
* Import the CTX class from ctx and initialize the ctx object:

```
const ctx = require('ctx-defense');
let ctxObject = new ctx;
```

* Protect a secret from an origin with a specific alphabet:

```
protectedSecret = ctxObject.Protect(secret, origin)
```

The origin parameter is optional.

* Retrieve the permutations for all origins:

```
permutations = ctxObject.getPermutations();
```

* For more information about how to use the ctx js library with express-handlebars
visit [here](https://github.com/dimkarakostas/ctx/tree/master/nodejs/express-handlebars-ctx/)

### Example

```
const ctx = require('./ctx');
let secret = 'A secret string';
let origin = 'user1'
let ctxObject = new ctx;

let permutation = ctxDefense.protect(secret,origin);
console.log('Permuted secret: ' + permutation.permuted + ' with originId ' +
    permutation.origin_id);

let perm = ctxDefense.getPermutations();

```
