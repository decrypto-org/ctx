flask-ctx
==============

A simple integration of the CTX defense against side-channel attacks for Flask projects.

Requirements
============

- Python 2.5+
- Flask 0.10+
- ctx-defense

Installation
============

- Install the latest stable version using ``pip``:

```sh
pip install flask-ctx
```

Configuration
=============

- Import the *ctx_processor* function from ctx's context processors:
```python
from flask_ctx.context_processors import ctx_processor
```

- Add the *ctx_processor* in the application's context processors:
```python
app.context_processor(ctx_processor)
```

Basic Usage
===========

- Use the *ctx_protect* function to use ctx on secrets:
```html
{{ ctx_protect(secret, origin, alphabet) }}
```

*secret* is a string containing the secret that needs to be protected and *origin*
is a string uniquely identifying the CTX origin for the secret. *alphabet* is
an optional argument to define the alphabet that the secret belongs to, default
being the [ASCII_printable](https://docs.python.org/2/library/string.html#string.printable) characters.

- Add the *ctx_permutations* function to include the used permutations for each
  origin:
```html
{{ ctx_permutations() }}
```

The *ctx_permutations* function needs to run after all *ctx_protect* calls
that use an origin for the first time. It is proposed that it is included
before the *</body>* HTML tag.

- Include the ctx *client script* in the template:
```html
<script src="ctx.js"></script>
```

Example
=======

```html
<!DOCTYPE html>

<html>

<head>
  <meta charset="utf-8">
  <title>flask-ctx Example</title>
</head>

<body>
  This is a very sensitive secret: {{ ctx_protect("a secret", "origin1") }}
  This is another very sensitive secret: {{ ctx_protect("another secret", "origin2") }}

  {{ ctx_permutations() }}
  <script src="ctx.js"></script>
</body>

</html>
```
