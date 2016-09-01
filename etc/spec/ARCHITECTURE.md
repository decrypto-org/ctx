CTX, Context Transformation Extension, is a cryptographic method which defends
against BREACH, CRIME, TIME, and generally any compression side-channel attack.
CTX uses context hiding in a per-origin manner to separate secrets from
different origins in order to avoid cross-compressibility.

Compression side-channel attacks is a domain that evolved greatly in recent
years. CTX fills the void as a generic defence that completely mitigates such
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
the CTX case, the secret alphabet is always the alphabet of ASCII bytes (0 -
128). Protected secrets are then permuted using the generated permutation prior
to transmission on the network by the server. Upon arrival on the client side,
the inverse permutation is applied to decode the secret. The same permutation
is applied to all secrets of the same origin. This is similar to a substitution
cipher. Note that the permuted text is always subsequently encrypted using
strong symmetric crypto such as AES over TLS.

The usage of origins on the response plaintext is the developer's
responsibility, the minimum being one origin for the entire response, in which
case CTX is not protecting any part of the plaintext, and the maximum being one
origin per character. The latter would result in the best possible security
under CTX, although compression would be effectively disabled possibly
resulting in poor performance. This is the case with defences such as [secret
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

# Django implementation

We provide an implementation for Django.

When using Django templating, use `ctx_protect` with an appropriate origin
parameter to protect your secret:

```python
    {% ctx_protect secret, "eve" %}
```

# node.js

We provide an implementation for node.js using the Express web framework and
mustache. To protect your secrets using mustache, use:

```js
    {{#ctx_protect "eve"}} {{secret}} {{/ctx_protect}}
```

# Client implementation

The client logic is implemented in ctx.js. It applies the inverse
transformations onload.
