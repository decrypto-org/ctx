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
