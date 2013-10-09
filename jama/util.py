#!/usr/bin/env python3
"""
Configuration parsing from
https://bitbucket.org/basti/python-amazon-product-api/

"""
try:
    from configparser import ConfigParser
except ImportError:
    from ConfigParser import SafeConfigParser as ConfigParser
import os

REQUIRED_KEYS = [
    'url',
    'account',
    'password',
]


CONFIG_FILES = [
    '/etc/jama.cfg',
    '~/.jama',
    '~/.jamarc'
]


def load_file_config(path=None):
    """
    Loads configuration from file with following content::

        [soap]
        url = <wsdl url endpoint>
        account = <username>
        password = <password>

    :param path: path to config file. If not specified, default locations of
    ``/etc/jama.cfg``, ``~/.jama``, and ``~/.jamarc`` are tried.
    """
    config = ConfigParser()
    if path is None:
        config.read([os.path.expanduser(path) for path in CONFIG_FILES])
    else:
        config.read(path)

    if not config.has_section('soap'):
        return {}

    return dict(
        (key, val)
        for key, val in config.items('soap')
        if key in REQUIRED_KEYS
    )


def load_environment_config():
    """
    Loads config dict from environmental variables (if set):

    * JAMA_URL
    * JAMA_USERNAME
    * JAMA_PASSWORD

    """
    mapper = {
        'url': 'JAMA_URL',
        'account': 'JAMA_USERNAME',
        'password': 'JAMA_PASSWORD',
    }
    return dict(
        (key, os.environ.get(val))
        for key, val in mapper.items()
        if val in os.environ
    )


def load_config(path=None):
    """
    Returns a dict with API credentials which is loaded from (in this order):

    * Environment variables ``JAMA_URL``, ``JAMA_USERNAME``, and
      ``JAMA_PASSWORD``
    * Config files ``/etc/jama.cfg`` or ``~/.jama`` or ``~/.jamarc``
      where the latter may add or replace values of the former.

    The returned dictionary may look like this::

        {
            'url': '<soap endpoint>',
            'account': '<account user name>',
            'password': 'super secret password'
        }

    :param path: path to config file.
    """
    config = load_file_config(path)
    config.update(load_environment_config())

    # substitute None for all values not found
    for key in REQUIRED_KEYS:
        if key not in config:
            config[key] = None

    return config
