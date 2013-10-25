#!/usr/bin/env python3
"""
9/10/13
"""

from setuptools import setup, find_packages

from jama.version import VERSION

setup(
    name = "python-jama",
    version = VERSION,
    description="A Python wrapper for the Jama API",
    long_description=open('README.md').read(),
    author=['Brian Thorne', 'Phillip Dixon', 'Donovan Johnson'],
    author_email=['bthorne@dynamiccontrols.com', 'pdixon@dynamiccontrols.com', 'djohnson@dynamiccontrols.com'],

    packages = find_packages(),
    scripts = [],
    install_requires = open('requirements.txt').read(),

    license="LGPL v3",
    keywords = "jama contour",
    url = "https://github.com/dynamiccontrols/python-jama/",   # project home page, if any

)