#!/usr/bin/env python

from setuptools import setup, find_packages


setup(
    name="ctx-defense",
    version="1.0.0",
    author="Dimitris Karakostas",
    author_email="dimit.karakostas@gmail.com",
    url="https://github.com/dimkarakostas/ctx",
    description="The CTX defense library.",
    long_description=open("README.rst").read(),
    download_url="https://github.com/dimkarakostas/ctx",
    license="MIT",
    packages=find_packages(exclude=['ctx_defense.tests']),
    test_suite='nose.collector',
    tests_require=['nose'],
    include_package_data=True,
    keywords="ctx defense compression security BREACH",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Topic :: Security",
        "Topic :: Security :: Cryptography",
    ],
    zip_safe=False,
)
