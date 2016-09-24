#!/usr/bin/env python

from setuptools import setup, find_packages


setup(
    name="django-ctx",
    version="1.0.0",
    author="Dimitris Karakostas",
    author_email="dimit.karakostas@gmail.com",
    url="https://github.com/dimkarakostas/ctx",
    description="A simple integration of the CTX defence against side-channel attacks for Django projects.",
    long_description=open("README.rst").read(),
    download_url="https://github.com/dimkarakostas/ctx",
    license="MIT",
    packages=find_packages(),
    include_package_data=True,
    keywords="django ctx defence compression security BREACH",
    install_requires=[
        "Django>=1.9",
        "ctx",
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
