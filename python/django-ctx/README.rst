django-ctx
==============

A simple integration of the CTX defense against side-channel attacks for Django projects.

Requirements
============

- Python 2.5+
- Django 1.9+
- ctx-defense

Installation
============

- Install the latest stable version using ``pip``:

```sh
pip install django-ctx
```

Configuration
=============

- Add ctx to your *INSTALLED_APPS* setting:
```python
INSTALLED_APPS = (
    ...
    'django_ctx',
)
```

- Ctx processes the *context* for template requests, which is implemented using a
 *context processor*. Add the ctx processor to your *context_processors* setting:
```python
context_processors = (
    ...
    'django_ctx.context_processors.ctx_protect',
)
```

Basic Usage
===========

- Load the ctx tag library:
```html
{% load ctx_tags %}
```

- Use the *ctx_protect* tag to use ctx on secrets:
```html
{% ctx_protect secret origin alphabet %}
```

*secret* is a string containing the secret that needs to be protected and *origin*
is a string uniquely identifying the CTX origin for the secret. *alphabet* is
an optional argument to define the alphabet that the secret belongs to, default
being 'ASCII' which refers to the [ASCII
printable](https://docs.python.org/2/library/string.html#string.printable) characters.

- Add the *ctx_permutations* tag to include the used permutations for each
  origin:
```html
{% ctx_permutations %}
```
 The *ctx_permutations* tag needs to be included after all *ctx_protect* tags
 that use an origin for the first time. It is proposed that it is included
 before the *</body>* HTML tag.

Example
=======
```html
<!DOCTYPE html>

<html>

<head>
  <meta charset="utf-8">
  <title>django-ctx Example</title>
</head>

<body>
  {% load ctx_tags %}

  This is a very sensitive secret from origin1: {% ctx_protect "my secret" "origin1" %}
  This is another very sensitive secret from origin2: {% ctx_protect "my other secret" "origin2" "ASCII_printable" %}

  {% ctx_permutations %}
</body>

</html>
```
