#!/usr/bin/env python

from setuptools import setup, find_packages


setup(
    name="django-ctx",
    version="1.0.0",
    author="Dimitris Karakostas",
    author_email="dimit.karakostas@gmail.com",
    url="https://github.com/dimkarakostas/ctx",
    description="A simple integration of the CTX defense against side-channel attacks for Django projects.",
    long_description=open("README.rst").read(),
    download_url="https://github.com/dimkarakostas/ctx",
    license="MIT",
    packages=find_packages(exclude=['django_ctx.tests']),
    test_suite='nose.collector',
    tests_require=['nose', 'Django>=1.9', 'ctx-defense'],
    include_package_data=True,
    keywords="django ctx defense compression security BREACH",
    install_requires=[
        "Django>=1.9",
        "ctx-defense",
    ],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Topic :: Security",
        "Topic :: Security :: Cryptography",
    ],
    zip_safe=False,
)
