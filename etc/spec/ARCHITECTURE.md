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

CTX depends on separate secrets based on origin. In this case, *origin* is used
to describe the party that generated each secret, either being web
application or user generated content.

CTX is used to protect secrets in HTML responses of web applications. Each
character in the plaintext response is considered a secret and should be
assigned to an origin. Using a keyed pseudo-random permutation function,
secrets are permuted using different permutations per origin. All characters
in the same origin will be compressed together, disabling cross-compression of
characters in different origins.

The usage of origins on the response plaintext is the developer's
responsibility, the minimum being one origin for the entire response, in which
case CTX is not protecting any part of the plaintext, and the maximum being one
origin per character. The latter would result in the best possible security
under CTX, although compression would be effectively disabled possibly
resulting in poor performance.
