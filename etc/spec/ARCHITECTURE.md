CTX, Context Transformation Extension, is a cryptographic method which defends
against BREACH, CRIME, TIME, and generally any compression side-channel attack.
CTX uses context hiding in a per-origin manner to separate secrets from
different origins in order to avoid cross-compressibility.

Compression side-channel attacks is a domain that evolved greatly in recent
years. CTX fills the void as a generic defense that completely mitigates such
attacks. Our aim is to create a production-level solution that enables web
services' administrators to strengthen web applications. It runs at the
application layer, is opt-in, and does not require modifications to web
standards or the underlying web server.

This document describes the architectural design of CTX implementations. It is
a recommended reading if you plan to contribute to CTX or implement it in new
web applications.

# Overview

CTX depends on separating secrets based on origin. In this case, *origin* is
used to describe the party that generated each secret, either being web
application or user generated content. (Do not confuse CTX origins with origins
of same-origin policy.) For any two secrets A and B annotated with the same
origin, it must hold true that the party able to change A would not violate the
application privacy contract by knowing B.

CTX is used to protect secrets in HTML and other content-type responses of web
applications as they travel on the network. The developer must decide which
portions of the response are sensitive and must be protected as secrets.
Sensitive data does not only include high-value secrets such as passwords and
CSRF tokens, but also user data that the developer wishes to keep private as
well as reflected data. For more information see [unexpected
secrets](https://ruptureit.com/blog/2016/07/27/unexpected-secrets-and-reflections/).

CTX protects only HTTPS responses, not HTTPS requests. Due to mitigations of
the CRIME attack, compression in HTTPS requests is always disabled, and hence
no protection against compression side-channel attacks is required.

A pseudo-random permutation of the secret alphabet is generated per origin. In
the CTX case, the secret alphabet can be the alphabet of ASCII bytes (0 - 128).
Protected secrets are then permuted using the generated permutation prior to
transmission on the network by the server. Upon arrival on the client side, the
inverse permutation is applied to decode the secret. The same permutation is
applied to all secrets of the same origin. This is similar to a substitution
cipher. Note that the permuted text is always subsequently encrypted using
strong symmetric crypto such as AES over TLS.

The usage of origins on the response plaintext is the developer's
responsibility, the minimum being one origin for the entire response, in which
case CTX is not protecting any part of the plaintext, and the maximum being one
origin per character. The latter would result in the best possible security
under CTX, although compression would be effectively disabled possibly
resulting in poor performance. This is the case with defenses such as [secret
masking](https://www.facebook.com/notes/protect-the-graph/preventing-a-breach-attack/1455331811373632/).

# Structure

The HTML response plaintext consists of a plain HTML structure along with
CTX-transformed parts. Each CTX part is annotated using an HTML *div* tag structured as:

```html
<div data-ctx-origin='i'>xyx</div>
```

where *i* is an integer.

Separately in the same response, JSON will be included like:

```json
[
    'abc',
    'cab',
    'bac',
    ...
]
```

'abc', 'cab', 'bac' are the permutations used to permute secrets of origin 0,
1, and 2 respectively. 'xyx' is the permuted data after applying permutation
for origin *i*.

In the inverse transformation, the client will calculate the secrets for all
permuted data and replace each instance of *data-ctx-origin* *divs* with the
plaintext that is generated using the inverse i-th permutation in the JSON.

The JSON is included in a `<script type="application/json"
id="ctx-permutations"></script>` tag at the HTML `<head></head>`.

# Python

The basic CTX functionality is implemented in the *ctx-defense* package. This
package defines the *app.py* and the *permuters.py* libraries. The
first defines the CTX class which is responsible for generating and
maintaining the permutations and applying them on secrets. The second defines
the permuter classes for different types of alphabets. As of this point, one
permuter for the ASCII printable alphabet exists.

In order to generate the permutations, the CTX class uses the
[random.shuffle](https://docs.python.org/2/library/random.html#random.shuffle)
function. This function uses the Fisher-Yates shuffle which is proven to be a
perfect shuffle given a good random number generator.

The CTX class provides the following API.

## API

#### available_permuters

A dictionary that defines the available permuters. The keys are strings that
identify the secret alphabet. The values are classes that implement the permuter
interface defined below.

#### protect

Apply CTX on a specific secret.

Arguments:

- secret: A string of the plaintext secret.
- origin: (Optional) A string defining uniquely the CTX origin for the secret.
  If no origin is specified, a random origin with an id string of 10 lowercase
  letters will be generated for this secret.
- secret_alphabet: (Optional) A string that identifies the alphabet of the
  secret. Must be in *available_permuters* keys. Default value is
  "ASCII_printable".

Applies the permutation that was generated for the *origin* on the *secret*. The
permutation is set the first time *protect* is called per origin. It is up to
the developer to define different origins in case multiple alphabets need to be
used.

Returns a dictionary with the following values:

- *origin_id*: an integer corresponding to the origin parameter.
- *permuted*: the permuted data using the permutation generated for the given
  origin.

#### get_permutations

Get all generated permutations.

Returns an array of strings. The i-th string in the array is the permutation for
the origin with origin_id=i.

## Permuters

Permuters are classes that implement the permutation functionality
for different secret alphabets. All permuters must implement the following
interface:

#### get_permutation

Returns a string containing the generated permutation for the alphabet. This
string defines a correlation of the plain alphabet and the permutation alphabet,
i.e. the first character of the permutation is used to replace the occurencies
of the first character of the plain alphabet in the secret etc.

#### permute

Applies the generated permutation on each character and returns the permuted data.

Arguments:
- secret: A string of the plaintext secret.

### Implemented permuters

- ASCII_printable: A permuter for the alphabet consisting of printable ASCII
  characters, as defined in
  [string.printable](https://docs.python.org/2/library/string.html#string.printable).

# Django implementation

We provide an implementation for Django.

When using Django templating, use `ctx_protect` with an appropriate origin
parameter to protect your secret:

```html
    {% ctx_protect "a secret", "an origin" %}
```
For more information on the Django CTX, visit the [django-ctx
repository](https://github.com/dimkarakostas/ctx/tree/master/etc/python/django-ctx).

# Flask implementation

We provide an implementation for Flask.

Use the `ctx_protect` function in your templates to protect a secret from a
specific origin.

```html
{{ ctx_protect("a secret", "an origin") }}
```

For more information on the Flask CTX, visit the [flask-ctx
repository](https://github.com/dimkarakostas/ctx/tree/master/etc/python/flask-ctx).

# node.js

We provide an implementation for node.js frameworks. The basic CTX
implementation is in *ctx-defense.js* in the [ctx-defense
folder](https://github.com/dimkarakostas/ctx/tree/master/nodejs/ctx-defense).

CTX defense can be used in many nodejs frameworks. It has been tested for
Express/express-handlebars, Express/pug, Express/EJS and Koa.js/koa-pug.
For more information on the nodejs-ctx-defense and its basic usage in the above
frameworks/templates visit the [nodejs-ctx-defense
folder](https://github.com/dimkarakostas/ctx/tree/master/nodejs/nodejs-ctx-defense).


# Client implementation

The client logic is implemented in ctx.js. It applies the inverse
transformations onload.
