ctx
==============

The CTX defence library.

Installation
============

- Install the latest stable version using ``pip``:

```sh
pip install ctx-defense
```

Basic Usage
===========

- Import the CTX class from ctx and initialize the ctx object:
```python
from ctx_defense import CTX

ctx_object = CTX()
```

- Protect a secret from an origin with a specific alphabet:
```python
protected_secret = ctx_object.protect(secret, origin, alphabet)
```

- Retrieve the permutations for all origins:
```python
permutations = ctx_object.get_permutations()
```

- For more information on the CTX library and the classes it implements visit the defence's [website](https://github.com/dimkarakostas/ctx).

Example
=======

```python
from ctx_defense import CTX

secret = 'A secret string'
origin = 'user1'
alphabet = 'ASCII'

ctx_object = CTX()
protected_secret = ctx_object.protect(secret, origin, alphabet)
permutations = ctx_object.get_permutations()
```
